import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PEP_URL
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all('li',
                                              attrs={'class': 'toctree-l1'})
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = soup.find('dl').text.replace('\n', ' ')
        results.append(
            (version_link, h1, dl)
        )
    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = soup.find('div', class_='sphinxsidebarwrapper')
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Ничего не нашлось')
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (link, version, status)
        )
    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = soup.find('div', {'role': 'main'})
    table_tag = main_tag.find('table', {'class': 'docutils'})
    pdf_a4_tag = table_tag.find('a', {'href': re.compile(r'.+pdf-a4\.zip$')})
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    peps = main_tag.find_all('tr')[1:]
    count_status = {}
    results = [('Статус', 'Количество')]
    for pep in peps:
        link = pep.a['href']
        pep_link = urljoin(PEP_URL, link)
        response = get_response(session, pep_link)
        soup = BeautifulSoup(response.text, 'lxml')
        card = find_tag(soup, 'section', {'id': 'pep-content'})
        card_dl = find_tag(card, 'dl', {'class': 'rfc2822 field-list simple'})
        for tag in card_dl:
            if tag.name == 'dt' and tag.text == 'Status:':
                status = tag.next_sibling.next_sibling.string
                status_chart = pep.td.text[1:]
                if status in count_status:
                    count_status[status] += 1
                else:
                    count_status[status] = 1
                if status[0] != status_chart:
                    logging.info(
                        '\nНесовпадающие статусы:\n'
                        f'{pep_link}\n'
                        f'Статус в карточке: {status}\n'
                        'Ожидаемые статусы:\n'
                        f'{EXPECTED_STATUS[status_chart]}\n'
                    )
    total = sum(count_status.values())
    for key, value in count_status.items():
        results.append((key, str(value)))
    results.append(('Total', str(total)))
    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()

from lxml import html
import requests
import connector

PAGE_DOMAIN = "https://libgen.is"
PAGE_DOMAIN_BK = "https://libgen.rs/"

PAGE_AMOUNT_TO_SCRAP = 10


class Scrapper:

  def scrap_list(self, connection, cursor):
    response = requests.get("https://libgen.is/fiction/?q=&criteria=&language=&format=")
    page = html.fromstring(response.text)

    pages_scrapped = 0
    while pages_scrapped < PAGE_AMOUNT_TO_SCRAP:
      book_links = page.xpath("//table[@class='catalog']//tbody//td/p/a/@href")
      
      for book_link in book_links:
        try:
          book_response = requests.get(PAGE_DOMAIN + book_link)
          book_page = html.fromstring(book_response.text)
        except:
          with open('errores.txt', 'a') as file:
            file.write(f'Error en link: {book_link}')
          try:
            book_response = requests.get(PAGE_DOMAIN_BK + book_link)
            book_page = html.fromstring(book_response.text)
          except:
            file.write(f'Error en ambos dominios: {book_link}')

        self.scrap_book(book_page, connection, cursor)

      page_url = self.next_page(page)
      print(page_url)
      response = requests.get(page_url)
      page = html.fromstring(response.text)

      pages_scrapped += 1

  def scrap_book(self, book_page, connection, cursor):
    data_wanted_array = ["Title", "Language", "Year", "ISBN", "File", "Time"]
    data_scrapped = list()

    for data_name in data_wanted_array:
      try:
        data_scrapped.append(book_page.xpath(f"//tr/td[contains(text(), '{data_name}')]/following-sibling::td[1]")[0].text)
      except:
        if data_name == data_wanted_array[2]:
          data_scrapped.append(0)
        else:
          data_scrapped.append("")

    try:
      data_scrapped.append(book_page.xpath(f"//tr/td//a[contains(@title, 'author')]")[0].text)
    except:
      data_scrapped.append("")

    try:    
      data_scrapped.append(book_page.xpath(f"//tr/td[contains(text(), 'Description')]/../following-sibling::tr[1]/td")[0].text)
    except:
      data_scrapped.append("")

    data_scrapped[1] = data_scrapped[1].split(";")[0]

    # Subir a la base
    print(f'{data_scrapped[0]}: {data_scrapped}')
    print('\n\n\n\n\n\n')

    sql = "INSERT INTO libros (Title, Book_Language, Book_Year, ISBN, File_url, Time_added_modified, Author, Book_Description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (data_scrapped[0],data_scrapped[1],data_scrapped[2],data_scrapped[3], data_scrapped[4], data_scrapped[5], data_scrapped[6], data_scrapped[7])
    cursor.execute(sql,val)
    connection.commit()

  def next_page(self, page):
    next_page_url = PAGE_DOMAIN + page.xpath("(//div[@class='catalog_paginator']/div/a/@href)[2]")[0]
    return next_page_url


def main():
  connection = connector.create_connector()
  cursor = connection.cursor()

  Scrapper().scrap_list(connection, cursor)


main()
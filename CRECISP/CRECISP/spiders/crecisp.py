# -*- coding: utf-8 -*-
import scrapy


class CrecispSpider(scrapy.Spider):
    name = 'crecisp'

    def start_requests(self):
        self.cookies = {
            '_ga': 'GA1.3.760870456.1582981260',
            'ASP.NET_SessionId': 'frzpillqyf5sqn5cpsiqjn0e',
            '_gid': 'GA1.3.520723151.1583815486',
            '_gat': '1',
        }

        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://www.crecisp.gov.br/cidadao/buscaporcorretores',
            b'Cache-Control': b'no-cache',
            b'Content-Type': b'text/html; charset=utf-8',
            b'Vary': b'Accept-Encoding',
            b'Server': b'Microsoft-IIS/7.5',
            b'X-Aspnetmvc-Version': b'5.2',
            b'X-Aspnet-Version': b'4.0.30319',
            b'X-Powered-By': b'ASP.NET',
            b'Date': b'Mon, 09 Mar 2020 15:18:46 GMT'
        }

        url = 'https://www.crecisp.gov.br/cidadao/listadecorretores?page=7748'

        yield scrapy.Request(url, cookies=self.cookies, dont_filter=True,
                             callback=self.get_crecis, headers=self.headers)

    def get_crecis(self, response):
        url = response.url
        proxima = ''#(response.css('a.navigate:contains(Próximo)::attr(href)')
                  # .get())
        crecis_all = response.css('.col-lg-4.broker-details')
        for creci in crecis_all:
            creci = creci.css('div span::text').getall()
            yield{
                'CRECI': creci[0],
                'Situação': creci[1],
                'URL': url
            }
        if proxima:
            url = f'https://www.crecisp.gov.br{proxima}'
            yield scrapy.Request(url, cookies=self.cookies, dont_filter=True,
                                 callback=self.get_crecis,
                                 headers=self.headers)

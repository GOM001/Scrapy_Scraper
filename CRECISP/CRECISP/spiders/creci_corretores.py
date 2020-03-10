# -*- coding: utf-8 -*-
import scrapy


class CreciCorretoresSpider(scrapy.Spider):
    name = 'creci_corretores'

    def start_requests(self):
        self.cookies = {
            '_ga': 'GA1.3.2017159564.1583724558',
            '_gid': 'GA1.3.445123655.1583724558',
            '_gat': '1',
            'ASP.NET_SessionId': 'qakeavvpialpd3x1avtk4dzv',
        }
        url = 'https://www.crecisp.gov.br/cidadao/corretordetalhes'

        with open('eggs.csv', 'r') as csvfile:
            spamwriter = csv.reader(csvfile)
            for creci in spamwriter:
                creci = creci[0].replace('|', '')
                formdata = {'registerNumber': creci.strip()}
                yield scrapy.FormRequest(url, formdata=formdata,   
                                         dont_filter=True, cookies=self.cookies,
                                         callback=self.get_corretores)
        def get_corretores(self, response):
            nome = response.css('.col-sm-9 h3::text').get()
            titulos = response.css('.col-sm-9 div strong label::text').getall()
            info = response.css('.col-sm-9 div span::text').getall()
            info_dict = {key: value for key, value in zip(titulos, info)}

            yield{
                'Nome': nome,
                'CRECI': info_dict.get('CRECI'),
                'Situação': info_dict.get('Situação'),
                'Município': info_dict.get('Município'),
                'UF': info_dict.get('UF'),
                'Contato': info_dict.get('Contato(s)'),
                'E-Mail': info_dict.get('E-Mail'),
                'E-Mail Oficial': info_dict.get('E-Mail Oficial')
            }


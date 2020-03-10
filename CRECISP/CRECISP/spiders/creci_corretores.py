# -*- coding: utf-8 -*-
import scrapy
import csv


class CreciCorretoresSpider(scrapy.Spider):
    name = 'creci_corretores'

    def start_requests(self):
        self.cookies = {
            '_ga': 'GA1.3.760870456.1582981260',
            'ASP.NET_SessionId': 'frzpillqyf5sqn5cpsiqjn0e',
            '_gid': 'GA1.3.520723151.1583815486',
            '_gat': '1',
        }

        url = 'https://www.crecisp.gov.br/cidadao/corretordetalhes'

        with open('crecisp.csv', 'r') as csvfile:
            spamwriter = csv.reader(csvfile)
            for creci in spamwriter:
                if creci[1].strip() == 'Ativo':
                    formdata = {'registerNumber': creci[0].strip()}
                    yield scrapy.FormRequest(url, formdata=formdata,   
                                            dont_filter=True, cookies=self.cookies,
                                            callback=self.get_corretores)
                else:
                    continue
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


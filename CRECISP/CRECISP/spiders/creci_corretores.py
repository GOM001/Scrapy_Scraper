# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


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
        processed = pd.read_csv('creci_det.csv', encoding='UTF-8')
        total = pd.read_csv('crecisp.csv',  encoding='UTF-8')
        processed_list = [item.strip() for item in processed['CRECI']]
        data_to_drop = total.loc[total['CRECI'].isin(processed_list)]

        data_to_process = total.drop(data_to_drop.index)

        for index, creci in data_to_process.iterrows():
            if creci.get('Situação').strip() == 'Ativo':
                formdata = {'registerNumber': creci.get('CRECI').strip()}
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

        if name:
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

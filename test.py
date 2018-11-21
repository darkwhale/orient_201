from utils import get_company_info
from utils import Company


def init():
    company1 = Company('db', 7.8)
    company2 = Company('zjs', 50)
    company3 = Company('zto', 100)
    company4 = Company('sf', 200)
    company5 = Company('jd', 250)
    company6 = Company('yd', 500)
    company7 = Company('yto', 700)
    company8 = Company('bsht', 800)
    company9 = Company('ss', 200)

    company_list = [company1, company2, company3, company4,
                    company5, company6, company7, company8, company9, ]

    return company_list


def test():
    company_list = init()
    a = get_company_info(company_list)
    for i in a:
        print(i)

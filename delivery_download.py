# Call URL - https://www.nseindia.com/api/historical/securityArchives?from=30-07-2022&to=30-07-2023&symbol=ITC&dataType=priceVolumeDeliverable&series=ALL

from db_tiny import get_all_symbols, save_data
from datetime import date, timedelta
import requests
# print(get_all_symbols())



def download_data(symbol, start_date, end_date):
    start = start_date.strftime("%d-%m-%Y")
    end = end_date.strftime("%d-%m-%Y")
    api_url = f"https://www.nseindia.com/api/historical/securityArchives?from={start}&to={end}&symbol={symbol}&dataType=priceVolumeDeliverable&series=ALL" 
    
    print(api_url)
    print('Hitting API')

    # baseurl = "https://www.nseindia.com/"

    # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
    #                      'like Gecko) '
    #                      'Chrome/80.0.3987.149 Safari/537.36',
    #        'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    
    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br', 
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Cache-Control': 'max-age=0',
        'Cookie': 'bm_sz=D39F4AA6388D8BE8A63B5A47B4030746~YAAQj88uF9y/6PCNAQAAp5pB9BbRorrFuRNx3YKI4dd5uopKuPdxq7vWlfEQWoP+8BMf0N5kJE4RWp/UtXZA/sxYIyHSgs7rqAI8/8XomHFFYaehpXt0zz8Lrz23o+bTtZREKCz2HVY3Vibw9lt9CXq1U7WDu5sI8Q7u1uXR6toRjXfS3H/kGCBwdKkzYrsxe0uNK+XFlUbjnbXd1K3mvYSbf8oi5BKHbzKlSPNptGMZ9PuUg0f417RtkjfosSSdgfTUa7PzBr/Bmvqqd+3Rb9mOHuaRS6mVz0pRK1Gg3sCOkQQ95wn4G+rKnFT084e9ay2nHGa3fNqJ/+UR/7FfYL8/ks3ONYTZmlIX2QJS5hvnPu/EcBi1~4273476~4474161; defaultLang=en; nsit=Yof0y6rULFv72vAuu5xOWvx1; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcwOTIwNzkwOCwiZXhwIjoxNzA5MjE1MTA4fQ.BQ73mzkqrmB_SAoSfxByluDSJQ8vtubm_hmb9ozu4E0; AKA_A2=A; ak_bmsc=4619C590886A125832D1EA8C0974CF81~000000000000000000000000000000~YAAQfF06Fyfk9e+NAQAAQPO69Bb56vihaYexRyMMVk2eScODhz67dSIqESRR17R7+cQ4DyM9vBeQs/Kb+R1jIVuw83oX7xtkCPlLEGdw7ub2sM572fuKRfGGXsPbw8D0g4tEd0TNLmVugJeEZ7B6KAAVSj30nuCiT/N87xfSWUUfW93XWYqaBKwYp7yIhZLqE8S2CjxKkb4+nRkdgLpSTMLL/KPfAVnIvg7IA9d6rddfquJV2+MFkD4d6FHVY1Ah3cmqD9e0e8BBKU7YoKHJGfHH2soQmHTICg/3hAM+Y0c60WtqipxKbCqerC/1dkipeGIwqf2Y3uJ1a0h95le3FZAhMAF0Sl8jUmU3IQ9BcPhNhm/R0Px6nPSESfan5bIA90mHlkusVieqSW4=; _abck=C4A30E5D0230A137EA53D4C26A6980C1~0~YAAQfF06F0zk9e+NAQAAxfa69Aua0kkMiF5vdk74Yz0GhKWyGOsG3oTwdeimm/xH1CbDSeQ6VAJ6z2mmZqUllkz/cIyDuRcOddjGdqDtq7vzVw6I6YyFs+29CEOpVohP57oDgcZ2jVCtt2/M2GL4EIlUvS8fXjuNqG9Rj7o2FfhOvJ6QQCxP/HlUMCiWDJgnz7AwCVYNktcYcSvdyMBi/h+fZNBLrSnKce76z2LjNRh44Fek9IZOVXai+OjgtKfIkqItll5d8hIfGazr2hUpraWxff/tcDtDiI2J4HsOf7K9Jp+JbYh728VRPQfPr8nTAcEtdI7BCrp2PFHW8JBTHRsspFEmR1jrNgNELh0fLHt8rM0zGR+mP3wa6UOh2KwcaArNRl9Nluvc4r9iDJlihBacDNTsGJevqE0=~-1~-1~-1; bm_sv=69070D0343F3EF031C821DFE7519A63F~YAAQfF06F83k9e+NAQAApwe79BbAtHxQ3oybXvKqtBqx1lkHgT4giuUrxajv4m2TbBOA9L3glqA2IbCZ6ax+SNe+riEfIOcPApdgDuergRaUpyPdZaXpPfolCvf25YCee7oBRDsf3kjh9GDd8Tc3G+bEjxM2n5voLVljNNsTUTaz50MuUjz+QM2ZnO+ltT4gX93kFTlcxleAd+87SklNmOkByu3XhDWJjHYSLgbhS5K+kglHgGmu6jO0eR+pH4mZkLQ=~1',
        'Dnt': '1',
        'Sec-Ch-Ua':'"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    session = requests.Session()
    # request = session.get(baseurl, headers=headers, timeout=5)
    # cookies = dict(request.cookies)
    response = session.get(api_url, headers=headers, timeout=5)

    # response = requests.get(api_url)

    api_data = response.json()
    print('Got API response')
    
    data = api_data['data']

    return data

def save(symbol, start_date, end_date):
    data = download_data(symbol, start_date, end_date)
    print(f"Got {len(data)} records from the API")
    save_data(data)



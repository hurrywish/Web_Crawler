def response(flow):
    if 'webdriver' in flow.response.text:
        print('webdriver')
        with open('/Users/hurrywish/Desktop/GitHub/Web_Crawler/Project3-RealAustralia/origin.txt','a') as fp:
            fp.write(flow.response.text)






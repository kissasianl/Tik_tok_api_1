# 17.06.2023


# General import
import requests, subprocess, re
from bs4 import BeautifulSoup




# Find parameter on url_site
def getParameter():

    # Variable
    token = ""

    # Get site of the url
    r = requests.get("https://snaptik.app")
    print("RESPONSE URL_SITE ", r.status_code)

    # Get soup
    soup = BeautifulSoup(r.text, "lxml")

    # Find token
    for el_input in soup.find_all("input"):
        if(el_input.get("name") == "token"):
            token = el_input.get("value")

    # Return cookie of the session
    return token

# Make request to site server
def make_req_server(token, url_video):

    # Header for request
    headers = {
        'authority': 'snaptik.app',
        'accept': '*/*',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'origin': 'https://snaptik.app',
        'referer': 'https://snaptik.app/',
        'sec-ch-ua': '"Opera";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin'
    }

    # Make request to get data from site with parameter
    response = requests.get('https://snaptik.app/abc2.php', headers=headers, params = {
        'url': url_video,
        'token': token
    })

    # Return
    return response

# Exctact variable for decode from req_server
def extract_variable(response):

    # Find variable to send to decoder 
    list_var = re.findall(r'\(\".*?,.*?,.*?,.*?,.*?.*?\)', response.text)

    # Add to list variable
    res_input = []
    for e in (list_var[0].split(",")):
        res_input.append(str(e).replace("(", "").replace(")", "").replace('"', ""))

    # Return
    return res_input

# Call decoder to get response from page
def call_decoder(result_list_variable):

    # Call decoder in node js 
    output = subprocess.check_output([
        'node', 'decode.js',
        str(result_list_variable[0]), str(result_list_variable[1]), str(result_list_variable[2]), str(result_list_variable[3]), str(result_list_variable[4]), str(result_list_variable[5])
    ])

    # Get result from decoder
    result = (output).decode("utf-8") 

    return result

# Exract url of video with soup
def get_url_video(html_page):

    # Soup result -> (result is html page)
    soup_res = BeautifulSoup(html_page, "lxml")

    # Collect all url from soup
    url_download_video = ""
    for a in soup_res.find_all("a"):

        url = a.get("href")
        url = str(url).replace('\\', "").replace('"', "")

        if("snaptik" in url): 
            url_download_video = url

    return url_download_video


# Main funtion
def main(url_video):

    # Get parameter to find token
    token = getParameter()
    print("TOKEN => ", token)

    # Make req server 
    response = make_req_server(token = token, url_video = url_video)
    print("RESPONSE SERVER => ", response.status_code)

    # Extract and get list of variable to decode
    result_list_variable = extract_variable(response)
    print("VARIABLE FIND => ", len(result_list_variable))

    # Call decoder with list of variable
    html_response = call_decoder(result_list_variable)

    # Get url of the video
    dd_url_video = get_url_video(html_response)

    print("VIDEO URL => ", dd_url_video)

    r = requests.get(dd_url_video)
    print("RESPONSE VIDEO => ", r.status_code)

    open(url_video.split("/")[-1] + ".mp4", "wb").write(r.content)

main(input("URL => "))
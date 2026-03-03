# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import os

# প্লাগিন হ্যান্ডেল এবং সেটিংস
addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path')
icon_path = os.path.join(addon_path, 'icon.png')
# ডিফল্ট ফ্যানআর্ট (যদি সার্ভারে কোনো ছবি না পাওয়া যায়)
default_fanart = os.path.join(addon_path, 'fanart.jpg') 

# ==============================
# 🎨 COLOR CONFIGURATION
# ==============================
CLR_CIRCLE = "gold"
CLR_DHAKA  = "deepskyblue"
CLR_MOVIE  = "lime"
CLR_ICC    = "orange"
CLR_KOREAN = "magenta"

# ==========================================
# 📂 FULL SERVER LIST (ALL SERVERS)
# ==========================================
SERVERS = [
    # --- CIRCLE FTP ---
    ("[COLOR %s][B]● CIRCLE:[/B][/COLOR] English Movies (2016-26)" % CLR_CIRCLE, "http://index2.circleftp.net/FILE/English%20%26%20Foreign%20Dubbed%20Movies/"),
    ("[COLOR %s][B]● CIRCLE:[/B][/COLOR] English Movies (1995-15)" % CLR_CIRCLE, "http://index.circleftp.net/FILE/English%20%26%20Foreign%20Dubbed%20Movies/"),
    ("[COLOR %s][B]● CIRCLE:[/B][/COLOR] South Hindi Dubbed (2000-23)" % CLR_CIRCLE, "http://ftp17.circleftp.net/FILE/Tamil%20Telugu%20%26%20Others%20Hindi%20Dubbed/"),
    ("[COLOR %s][B]● CIRCLE:[/B][/COLOR] South Hindi Dubbed (2024-26)" % CLR_CIRCLE, "http://ftp13.circleftp.net/FILE/Tamil%20Telugu%20%26%20Others%20Hindi%20Dubbed/"),
    ("[COLOR %s][B]● CIRCLE:[/B][/COLOR] Hindi Movies" % CLR_CIRCLE, "http://index1.circleftp.net/FILE/Hindi%20Movies/"),
    ("[COLOR %s][B]● CIRCLE:[/B][/COLOR] Dubbed TV Series" % CLR_CIRCLE, "http://ftp16.circleftp.net/FILE/Dubbed%20TV%20Series%20%26%20Shows/"),
    
    # --- DHAKAFLIX ---
    ("[COLOR %s][B]● DHAKAFLIX:[/B][/COLOR] English (1080p)" % CLR_DHAKA, "http://172.16.50.14/DHAKA-FLIX-14/English%20Movies%20%281080p%29/"),
    ("[COLOR %s][B]● DHAKAFLIX:[/B][/COLOR] English Standard" % CLR_DHAKA, "http://172.16.50.7/DHAKA-FLIX-7/English%20Movies/"),
    ("[COLOR %s][B]● DHAKAFLIX:[/B][/COLOR] Hindi Movies" % CLR_DHAKA, "http://172.16.50.14/DHAKA-FLIX-14/Hindi%20Movies/"),
    ("[COLOR %s][B]● DHAKAFLIX:[/B][/COLOR] South Dubbed" % CLR_DHAKA, "http://172.16.50.14/DHAKA-FLIX-14/SOUTH%20INDIAN%20MOVIES/Hindi%20Dubbed/"),
    ("[COLOR %s][B]● DHAKAFLIX:[/B][/COLOR] Kolkata Bangla" % CLR_DHAKA, "http://172.16.50.7/DHAKA-FLIX-7/Kolkata%20Bangla%20Movies/"),
    ("[COLOR %s][B]● DHAKAFLIX:[/B][/COLOR] Foreign Language" % CLR_DHAKA, "http://172.16.50.7/DHAKA-FLIX-7/Foreign%20Language%20Movies/"),
    
    # --- MOVIE DATA (10.1.1.1) ---
    ("[COLOR %s][B]● MOVIE-DATA:[/B][/COLOR] English 1080p" % CLR_MOVIE, "http://10.1.1.1/data/English%20Movies%20(1080p)/"),
    ("[COLOR %s][B]● MOVIE-DATA:[/B][/COLOR] Hindi Movies" % CLR_MOVIE, "http://10.1.1.1/data/Hindi%20Movies/"),
    ("[COLOR %s][B]● MOVIE-DATA:[/B][/COLOR] South Dubbed" % CLR_MOVIE, "http://10.1.1.1/data/SOUTH%20INDIAN%20MOVIES/Hindi%20Dubbed/"),
    ("[COLOR %s][B]● MOVIE-DATA:[/B][/COLOR] IMDB Top 250" % CLR_MOVIE, "http://10.1.1.1/data/IMDb%20Top-250%20Movies/"),
    ("[COLOR %s][B]● MOVIE-DATA:[/B][/COLOR] Animation (1080p)" % CLR_MOVIE, "http://10.1.1.1/data/Animation%20Movies%20%281080p%29/"),
    ("[COLOR %s][B]● MOVIE-DATA:[/B][/COLOR] Animation Standard" % CLR_MOVIE, "http://10.1.1.1/data/Animation%20Movies/"),
    
    # --- KOREAN ---
    ("[COLOR %s][B]● KOREAN:[/B][/COLOR] Web Series" % CLR_KOREAN, "http://172.16.50.14/DHAKA-FLIX-14/KOREAN%20TV%20%26%20WEB%20Series/"),
    
    # --- ICC-FTP ---
    ("[COLOR %s][B]● ICC-FTP:[/B][/COLOR] Server S10" % CLR_ICC, "http://10.16.100.202/ftps10/"),
    ("[COLOR %s][B]● ICC-FTP:[/B][/COLOR] Server S3" % CLR_ICC, "http://10.16.100.206/ftps3/"),
    ("[COLOR %s][B]● ICC-FTP:[/B][/COLOR] Server S12" % CLR_ICC, "http://10.16.100.212/iccftps12/"),
    ("[COLOR %s][B]● ICC-FTP:[/B][/COLOR] Server S13" % CLR_ICC, "http://10.16.100.213/iccftps13/"),
    ("[COLOR %s][B]● ICC-FTP:[/B][/COLOR] Server S14" % CLR_ICC, "http://10.16.100.214/iccftps14/"),
]

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href and href not in ['../', './', '/'] and not href.startswith('?'):
                self.links.append(href)

def get_links(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            parser = LinkParser()
            parser.feed(html)
            return parser.links
    except:
        return []

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def list_root_servers():
    for name, url in SERVERS:
        list_item = xbmcgui.ListItem(label=name)
        list_item.setArt({'icon': icon_path, 'thumb': icon_path, 'fanart': default_fanart})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=build_url({'url': url}), listitem=list_item, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def list_items(url):
    links = get_links(url)
    
    # সার্ভার থেকে ইমেজ ফাইল খুঁজে বের করা (যেমন: a_AL_.jpg)
    image_files = [l for l in links if l.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    current_poster = icon_path
    current_fanart = default_fanart
    
    if image_files:
        img_path = urllib.parse.urljoin(url, image_files[0])
        current_poster = img_path
        current_fanart = img_path

    for link in links:
        full_url = urllib.parse.urljoin(url, link)
        display_name = urllib.parse.unquote(link).rstrip('/')
        display_name = os.path.basename(display_name)

        if link.endswith('/'):
            f_name = "[COLOR skyblue]📁 %s[/COLOR]" % display_name
            list_item = xbmcgui.ListItem(label=f_name)
            # ফ্যানআর্ট যুক্ত করা হয়েছে যাতে ব্যাকগ্রাউন্ডে ছবি দেখায়
            list_item.setArt({'icon': "DefaultFolder.png", 'thumb': current_poster, 'fanart': current_fanart})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=build_url({'url': full_url}), listitem=list_item, isFolder=True)
            
        elif link.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.ts')):
            v_name = "[COLOR springgreen]▶ %s[/COLOR]" % display_name
            list_item = xbmcgui.ListItem(label=v_name)
            list_item.setInfo('video', {'title': display_name, 'mediatype': 'movie'})
            list_item.setArt({'icon': "DefaultVideo.png", 'thumb': current_poster, 'fanart': current_fanart})
            list_item.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=full_url, listitem=list_item, isFolder=False)

    xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(addon_handle)

def router(paramstring):
    params = urllib.parse.parse_qs(paramstring)
    url = params.get('url', [None])[0]
    if url:
        list_items(url)
    else:
        list_root_servers()

if __name__ == '__main__':
    router(sys.argv[2][1:])

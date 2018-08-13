#!/usr/bin/python
import re
import sys
import json
import getopt
import socket
import urllib2
import dns.resolver
from urllib2 import urlopen

country = {'AF': 'Afghanistan', 'AX': 'Aland', 'AL': 'Albania', 'DZ': 'Algeria', 'AS': 'American Samoa', 'AD': 'Andorra',\
           'AO': 'Angola', 'AI': 'Anguilla', 'AQ': 'Antarctica', 'AG': 'Antigua and Barbuda', 'AR': 'Argentina', 'AM': 'Armenia',\
           'AW': 'Aruba', 'AC': 'Ascension Island', 'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaijan', 'BS': 'Bahamas',\
           'BH': 'Bahrain', 'BD': 'Bangladesh', 'BB': 'Barbados', 'EUS': 'Basque Country', 'BY': 'Belarus', 'BE': 'Belgium',\
           'BZ': 'Belize', 'BJ': 'Benin', 'BM': 'Bermuda', 'BT': 'Bhutan', 'BO': 'Bolivia', 'BQ': 'Bonaire', 'BA': 'Bosnia and Herzegovina',\
           'BW': 'Botswana', 'BV': 'Bouvet Island', 'BR': 'Brazil', 'IO': 'British Indian Ocean Territory', 'VG': 'British Virgin Islands',\
           'BN': 'Brunei', 'BG': 'Bulgaria', 'BF': 'Burkina Faso', 'MM': 'Myanmar', 'BI': 'Burundi', 'KH': 'Cambodia',\
           'CM': 'Cameroon', 'CA': 'Canada', 'CV': 'Cape Verde', 'CAT': 'Catalonia', 'KY': 'Cayman Islands', 'CF': 'Central African Republic',\
           'TD': 'Chad', 'CL': 'Chile', 'CN': 'China', 'CX': 'Christmas Island', 'CC': 'Cocos (Keeling) Islands', 'CO': 'Colombia',\
           'KM': 'Comoros', 'CD': 'Congo (Congo-Kinshasa)', 'CG': 'Congo (Congo-Brazzaville)', 'CK': 'Cook Islands', 'CR': 'Costa Rica', 'CI': 'Cote d\'Ivoire',\
           'HR': 'Croatia', 'CU': 'Cuba', 'CW': 'Curacao', 'CY': 'Cyprus', 'CZ': 'Czechia', 'DK': 'Denmark',\
           'DJ': 'Djibouti', 'DM': 'Dominica', 'DO': 'Dominican Republic', 'TL': 'East Timor (Timor-Leste)', 'TP': 'Timor Portugues', 'EC': 'Ecuador',\
	   'EG': 'Egypt', 'SV': 'El Salvador', 'GQ': 'Equatorial Guinea', 'ER': 'Eritrea', 'EE': 'Estonia', 'ET': 'Ethiopia',\
           'EU': 'European Union', 'FK': 'Falkland Islands', 'FO': 'Faeroe Islands', 'FM': 'Federated States of Micronesia', 'FJ': 'Fiji', 'FI': 'Finland',\
           'FR': 'France', 'GF': 'French Guiana', 'PF': 'French Polynesia', 'TF': 'French Southern and Antarctic Lands', 'GA': 'Gabon', 'GAL': 'Galicia',\
           'GM': 'Gambia', 'PS': 'Palestine (GAZA STRIP)', 'GE': 'Georgia', 'DE': 'Germany', 'GH': 'Ghana', 'GI': 'Gibraltar',\
           'GR': 'Greece', 'GL': 'Greenland', 'GD': 'Grenada', 'GP': 'Guadeloupe', 'GU': 'Guam', 'GT': 'Guatemala',\
           'GG': 'Guernsey', 'GN': 'Guinea', 'GW': 'Guinea-Bissau', 'GY': 'Guyana', 'HT': 'Haiti', 'HM': 'Heard Island and McDonald Islands',\
           'HN': 'Honduras', 'HK': 'Hong Kong', 'HU': 'Hungary', 'IS': 'Iceland', 'IN': 'India', 'ID': 'Indonesia',\
           'IR': 'Islamic Republic of Iran', 'IQ': 'Iraq', 'IE': 'Ireland', 'IM': 'Isle of Man', 'IL': 'Israel', 'IT': 'Italy',\
           'JM': 'Jamaica', 'JP': 'Japan', 'JE': 'Jersey', 'JO': 'Jordan', 'KZ': 'Kazakhstan', 'KE': 'Kenya',\
           'KI': 'Kiribati', 'KW': 'Kuwait', 'KG': 'Kyrgyzstan', 'LA': 'Laos', 'LV': 'Latvia',\
           'LB': 'Lebanon', 'LS': 'Lesotho', 'LR': 'Liberia', 'LY': 'Libya', 'LI': 'Liechtenstein', 'LT': 'Lithuania',\
           'LU': 'Luxembourg', 'MO': 'Macau', 'MK': 'Macedonia', 'MG': 'Madagascar', 'MW': 'Malawi', 'MY': 'Malaysia',\
           'MV': 'Maldives', 'ML': 'Mali', 'MT': 'Malta', 'MH': 'Marshall Islands', 'MQ': 'Martinique', 'MR': 'Mauritania',\
           'MU': 'Mauritius', 'YT': 'Mayotte', 'MX': 'Mexico', 'MD': 'Moldova', 'MC': 'Monaco', 'MN': 'Mongolia',\
           'ME': 'Montenegro', 'MS': 'Montserrat', 'MA': 'Morocco', 'MZ': 'Mozambique', 'MM': 'Myanmar', 'NA': 'Namibia',\
           'NR': 'Nauru', 'NP': 'Nepal', 'NL': 'Netherlands', 'NC': 'New Caledonia', 'NZ': 'New Zealand', 'NI': 'Nicaragua',\
           'NE': 'Niger', 'NG': 'Nigeria', 'NU': 'Niue', 'NF': 'Norfolk Island', 'KP': 'North Korea', 'MP': 'Northern Mariana Islands',\
           'NO': 'Norway', 'OM': 'Oman', 'PK': 'Pakistan', 'PW': 'Palau', 'PA': 'Panama', 'PG': 'Papua New Guinea',\
           'PY': 'Paraguay', 'PE': 'Peru', 'PH': 'Philippines', 'PN': 'Pitcairn Islands', 'PL': 'Poland', 'PT': 'Portugal',\
           'PR': 'Puerto Rico', 'QA': 'Qatar', 'RO': 'Romania', 'RU': 'Russia', 'RW': 'Rwanda', 'RE': 'Reunion Island',\
           'SH': 'Saint Helena', 'KN': 'Saint Kitts and Nevis', 'LC': 'Saint Lucia', 'PM': 'Saint-Pierre and Miquelon', 'VC': 'Saint Vincent and the Grenadines',\
           'WS': 'Samoa', 'SM': 'San Marino', 'ST': 'Sao Tome and Principe', 'SA': 'Saudi Arabia', 'SN': 'Senegal', 'RS': 'Serbia',\
           'SC': 'Seychelles', 'SL': 'Sierra Leone', 'SG': 'Singapore', 'SK': 'Slovakia', 'SI': 'Slovenia', 'SB': 'Solomon Islands',\
           'SO': 'Somalia', 'ZA': 'South Africa', 'GB': 'Great Britain', 'GS': 'South Georgia and the South Sandwich Islands', 'KR': 'South Korea', 'SS': 'South Sudan',\
           'ES': 'Spain', 'LK': 'Sri Lanka', 'SD': 'Sudan', 'SR': 'Suriname', 'SJ': 'Svalbard and Jan Mayen Islands', 'SZ': 'Swaziland', 'SE': 'Sweden',\
           'CH': 'Switzerland', 'SY': 'Syria', 'TW': 'Taiwan', 'TJ': 'Tajikistan', 'TZ': 'Tanzania', 'TH': 'Thailand',\
           'TG': 'Togo', 'TK': 'Tokelau', 'TO': 'Tonga', 'TT': 'Trinidad & Tobago', 'TN': 'Tunisia', 'TR': 'Turkey',\
           'TM': 'Turkmenistan', 'TC': 'Turks and Caicos Islands', 'TV': 'Tuvalu', 'UG': 'Uganda', 'UA': 'Ukraine', 'AE': 'United Arab Emirates (UAE)',\
           'UK': 'United Kingdom (UK)', 'US': 'United States of America (USA)', 'VI': 'United States Virgin Islands', 'UY': 'Uruguay', 'UZ': 'Uzbekistan',\
           'VU': 'Vanuatu', 'VA': 'Vatican City', 'VE': 'Venezuela', 'VN': 'Vietnam', 'WF': 'Wallis and Futuna', 'EH': 'Western Sahara',\
           'YE': 'Yemen', 'ZM': 'Zambia', 'ZW': 'Zimbabwe', 'COM': 'GLOBAL', 'NET': 'GLOBAL', 'ORG': 'GLOBAL', 'INFO': 'GLOBAL', 'SHOP': 'GLOBAL', 'HEALTH': 'GLOBAL',\
           'CLICK': 'GLOBAL', 'HOST': 'GLOBAL'
        }

def start(target_lst, info, ns_records, alexa_rank, tld, green, cyan, red, nc):
    if target_lst:
        for each_target in target_lst:
            print green + '   [+] ' + each_target + nc
            ip = get_ip(each_target)
            result = get_result(ip)
            digging(result, each_target, info, ns_records, alexa_rank, tld, green, cyan, red, nc)

def all_targets(target_file, single_target):
    targets = list()
    target_lst = list()
    if target_file:
        targets = [line.strip('\n') for line in open(target_file)]

    if single_target:
        targets.append(single_target)

    for t in targets:
        if 'http://' in t or 'https://' in t:
            t = t.split('/')[2]
        if t.startswith('www.'):
            t = t.replace('www.', '')
        target_lst.append(t)

    return list(set(target_lst))

def get_ip(target):
    ip = socket.gethostbyname(target)
    return ip

def get_result(ip):
    ip_info = 'https://ipinfo.io/' + ip + '/json'
    if ip_info is not None:
        response = urlopen(ip_info)
        result = json.load(response)
        return result

def get_info(target, result):
    res_params = list()
    all_params = ['ip', 'hostname', 'city', 'region', 'country', 'loc', 'postal', 'org']
    for r in result.keys():
        res_params.append(r.encode())
    return all_params, res_params

def get_records(target):
    response = dns.resolver.query(target, 'NS')
    return response 

def get_alexa(target):
    data = urllib2.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (target)).read()
    country_rank = re.findall("COUNTRY[^\d]*(\d+)", data)
    global_rank = re.findall("REACH[^\d]*(\d+)", data)
    if country_rank:
        country_rank = country_rank[0]
    else:
        country_rank = '-'

    if global_rank:
        global_rank = global_rank[0]
    else:
        global_rank = '-'

    return global_rank, country_rank

def get_tld(target):
    tld = target.split('.')[-1].upper()
    return tld

def digging(result, target, info, ns_records, alexa_rank, tld, green, cyan, red, nc):
    global country
    if tld:
        try:
            tld = get_tld(target)
            print '\t' + blue + 'TLD: ' + cyan + '.' + tld.lower() + ', ' + country[tld] + nc + '\n'
        except Exception:
            print '\t' + blue + 'TLD: ' + cyan + '-' + nc + '\n'

    if info:
        all_params, res_params = get_info(target, result)
        for a in all_params:
            if a in res_params and result[a] != '':
                if a.upper() == 'COUNTRY':
                    print '\t' + blue + a.upper() + ': ' + cyan + country[result[a]] + nc
                else:
                    print '\t' + blue + a.upper() + ': ' + cyan + result[a] + nc
        print

    if ns_records:
        try:
            response = get_records(target)
            if response:
                for t in response:
                    ns = t.to_text()
                    nsip = socket.gethostbyname(ns)
                    print '\t' + blue + 'NS: ' + cyan + ns + nc
                    result = get_result(nsip)
                    all_params, res_params = get_info(target, result)
                    for a in all_params:
                        if a in res_params and result[a] != '':
                            if a.upper() == 'COUNTRY':
                                print '\t\t' + blue + a.upper() + ': ' + cyan + country[result[a]] + nc
                            else:
                                print '\t\t' + blue + a.upper() + ': ' + cyan + result[a] + nc
                    print
                print
        except Exception as err:
            pass

    if alexa_rank:
        data = get_alexa(target)
        if data:
            global_rank , country_rank = data
            print '\t' + blue + 'COUNTRY RANK: ' + cyan + country_rank + nc
            print '\t' + blue + 'GLOBAL RANK: ' + cyan + global_rank + nc + '\n'
    print

def usage(blue, nc):
        print green + "          ____  _                        "
        print "         |  _ \(_) __ _  __ _  ___ _ __          "
        print "         | | | | |/ _` |/ _` |/ _ \ '__|         "
        print "         | |_| | | (_| | (_| |  __/ |            "
        print "         |____/|_|\__, |\__, |\___|_|            "
        print "                  |___/ |___/   " + nc + "\n"
        print blue + "By: Arshatech.com"
        print "Usage: python %s [options]" % sys.argv[0] + "\n"
        print "       -h, --help             Print this help summary page."
        print "       -t:, --target=         Get one ip address or website."
        print "       -l:, --target-list=    Get ip address or website list."
        print "                                     The file contains ip addresses or websites."
        print "                                     The true file format is one address per line."
        print "       -i, --info             Print information of website or ip."
        print "       -n, --ns-records       Print name servers of website."
        print "       -a, --alexa-rank       Enable printing ip address or website alexa rank."
        print "       -e, --extension        Print country name of given domain extension."
        print
        print "Example:"
        print "       python %s -t google.com -enai" % sys.argv[0]
        print "       python %s -l domain.lst -i" % sys.argv[0] + "\n" + nc

def color():
    colors = {'green':'\x1b[1;32m', 'dark_green':'\x1b[0;32m', 'red':'\x1b[1;31m', 'blue':'\x1b[1;34m', 'cyan':'\x1b[1;36m', 'yellow':'\x1b[1;33m', 'no_color':'\x1b[0m'}
    blue = colors.values()[0]
    dark_green = colors.values()[1]
    yellow = colors.values()[2]
    green = colors.values()[3]
    nc = colors.values()[4]
    cyan = colors.values()[5]
    red = colors.values()[6]
    return blue, yellow, green, cyan, red, nc

if __name__ == '__main__':
    blue, yellow, green, cyan, red, nc = color()
    if len(sys.argv) <= 2:
        usage(blue, nc)
        sys.exit(1)
    else:
        try:
            opts, args = getopt.getopt(sys.argv[1:],'t:l:inaeh',['target=', 'target-list=', 'info', 'ns-records', 'alexa-rank', 'extension', 'help'])
            if len(opts) == 0:
                usage(blue, nc)
                sys.exit()
        except getopt.GetoptError:
            usage(blue, nc)
            sys.exit()

        single_target = None
        target_file = None
        tld = None
        info = False
        ns_records = False
        alexa_rank = False
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                usage(blue, nc)
                sys.exit()
            elif opt == '-t' or opt == '--target':
                single_target = str(arg)
            elif opt == '-l' or opt == '--target-list':
                target_file = str(arg)
            elif opt == '-i' or opt == '--info':
                info = True
            elif opt == '-n' or opt == '--ns-records':
                ns_records = True
            elif opt == '-a' or opt == '--alexa-rank':
                alexa_rank = True
            elif opt == '-e' or opt == '--extension':
                tld = True

        if single_target or target_file:
            if not info and not ns_records and not alexa_rank and not tld:
                usage(blue, nc)
                sys.exit()

        try:
            target_lst = all_targets(target_file, single_target)
            print blue + ' [~] By: Arshatech.com' + nc
            start(target_lst, info, ns_records, alexa_rank, tld, green, cyan, red, nc)
        except KeyboardInterrupt:
            print yellow + ' [*] Exiting program...' + nc + '\n'
            sys.exit()
        except Exception as err:
            print red + '   [-] Error: %s ' %err + nc + '\n'
            sys.exit()

import dateutil.parser

def change_date_format(datestr):
    datestr = datestr.split(',')[0]
    parsed_date = dateutil.parser.parse(datestr)
    return datestr

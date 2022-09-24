import re

dateRegExs = [#Sample date dd-Apr|April-yyyy or dd Apr|April yyyy
r"(.*\s?\d{1,2}(\s|-)(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)(\s|-)+\d{4}\s)"
#Sample date :: dd/mm/yyyy(space) dd-mm-yyyy(space) dd.mm.yyyy(space) or mm/dd/yyyy(space)  d/m/yyyy
,r"(^\d{1,2}[.\/-]\d{1,2}[.\/-]\d{4}\s)"
,r"(^.*\d{1,2}[.\/-]\d{1,2}[.\/-]\d{4}\s)"
# Sample date mm/dd/yyyy or mm-dd-yyyy or mm.dd.yyyy
,r"(^.*\s((0)[0-9])|((1)[0-2])[-.\/](([0-2][0-9]|(3)[0-1]))[-.\/]\d{4}$)"
# Sample date dd/mm/yyyy or dd-mm-yyyy or dd.mm.yyyy
,r"(^.*\s(([0-2][0-9]|(3)[0-1]))[-.\/]((0)[0-9])|((1)[0-2])[-.\/]\d{4}$)"
# Smaple date  April 1, 2019 
,r"(.*\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}\s)"
,r"(.*\d{1,2}(st|nd|rd|th)\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{4}\s)"
]

dateRegExTosearch =[r"\d{1,2}\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{4}",
r"(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}",
r"\d{1,2}-(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)-+\d{2}",
r"\d{1,2}-(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)-+\d{4}",
r"\d{1,2}[-.\/]\d{1,2}[-.\/]\d{4}",
r"\d{1,2}[-.\/]\d{1,2}[-.\/]\d{2}",
r"\d{1,2}(st|nd|rd|th)\s(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|Aprial|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{4}"
]
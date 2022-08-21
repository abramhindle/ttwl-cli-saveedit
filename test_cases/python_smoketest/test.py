from ttwlsave.ttwlsave import TTWLSave
s = TTWLSave("2.sav")
item = s.create_new_item_encoded("WL(BQAAAAD2GoC6/CzggUoUCqetGZJDPC4BAAAA)")
print(item.eng_name)
item2 = s.create_new_item_encoded("BL3(BQAAAAD2GoC6/CzggUoUCqetGZJDPC4BAAAA)")
print(item2.eng_name)
# import sys
# sys.exit(1)

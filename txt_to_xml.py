import re
import xml.etree.ElementTree as ET
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

rex = re.compile(r'''(?P<title>Name
	|Type
	|Serving
	|Ingredients
	|Preparation
	|Cooking+\s+Time
	)
	\s*:?\s*
	(?P<value>.*)
	''', re.VERBOSE)
root = ET.Element('root')
root.text = '\n'    

global switch

with open('re') as f:
	switch = 1
	recipe = ET.SubElement(root, 'recipe')
	recipe.text = '\n'    
	recipe.tail = '\n\n'  
	for line in f:
		if line == "\n":
			continue

		line = line.strip()

		m = rex.search(line)
	
		if m:
			title = m.group('title')
			title = title.replace('&', '')
			title = title.replace(' ', '')
			
			if line.startswith('Ingredients'):
				ingredients = ET.SubElement(recipe, 'ingredients')
				ingredients.text = '\n'
				ingredients.tail = '\n'
			elif (line.startswith('Preparation')):
				preparation =  ET.SubElement(recipe, 'preparation')
				preparation.text = '\n'
				preparation.tail = '\n'
				switch = 0


			else:
				e = ET.SubElement(recipe, title.lower())
				e.text = m.group('value')
				e.tail = '\n'
		else:
			if(switch):
				print "In item"
				item = ET.SubElement(ingredients, 'item')
				item.text = line
				item.tail = '\n'
			else:
				print "In step"
				step = ET.SubElement(preparation, 'step')
				step.text = line
				step.tail = '\n'
                


tree = ET.ElementTree(root)
tree.write('cell.xml', encoding='utf-8', xml_declaration=True)

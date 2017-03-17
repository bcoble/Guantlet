from lxml import html
import requests

## Fields
base_url = 'https://www.mtggoldfish.com'
modern_url = '/metagame/modern/full'
# deck - base/decklink

modern_decks = []

def crawlWebPage():
	print 'Crawling page'
	
	page = requests.get(base_url + modern_url)
	tree = html.fromstring(page.content)

	archetypeTileXpath = '//div[2]/div/h2/span/a'
	tileNodes = sorted(set(tree.xpath(archetypeTileXpath)))
	#print tileNodes[0].xpath('@href')
	#print tileNodes[0].xpath('text()')
	
	# Can now loop over all links and decks
	for node in tileNodes:
		deckname = node.xpath('text()')[0]
		decklink = node.xpath('@href')[0]
		readAndSaveDeckList(deckname, base_url + decklink)

def readAndSaveDeckList(deckName, deckLink):
	print deckName, deckLink

	f = open('modernDecks/'+
		deckName.replace(' ','').replace('\'','').replace('/','')+
		'.txt', 'w')
	f.truncate()


	page = requests.get(deckLink)
	tree = html.fromstring(page.content)

	table = tree.xpath('//div/div[@id="tab-online"]/div//table[@class="deck-view-deck-table"]/tr')
	print 'Mainboard'

	for tr in table:
		td = tr.xpath('td')
		if len(td) == 1: 
			text = td[0].text.strip().replace('\n','')
			if text[:-4] == 'Sideboard':
				print 'Sideboard'
				f.write('\nSideboard\n')
		elif len(td) == 4:
			card = getCardName(td)

	f.close()


def getCardName(td):
	card = {}
	card['count'] = td[0].text.strip()
	if (len(td[1].xpath('a')) > 0):
		card['cardname'] = td[1].xpath('a')[0].text
	elif (td[1].text.strip() == 'Breaking' || td[1].text.strip() == 'Entering'):
		card['cardname'] = 'Breaking/Entering'
	elif (td[1].text.strip() == 'Wear' || td[1].text.strip() == 'Tear'):
		card['cardname'] = 'Wear/Tear'
	elif (td[1].text.strip() == 'Catch' || td[1].text.strip() == 'Release'):
		card['cardname'] = 'Catch/Release'
	elif (td[1].text.strip() == 'Alive' || td[1].text.strip() == 'Well'):
		card['cardname'] = 'Alive/Well'
	elif (td[1].text.strip() == 'Armed' || td[1].text.strip() == 'Dangerous'):
		card['cardname'] = 'Armed/Dangerous'
	elif (td[1].text.strip() == 'Wear' || td[1].text.strip() == 'Tear'):
		card['cardname'] = 'Wear/Tear'
	elif (td[1].text.strip() == 'Far' || td[1].text.strip() == 'Away'):
		card['cardname'] = 'Far/Away'
	elif (td[1].text.strip() == 'Beck' || td[1].text.strip() == 'Call'):
		card['cardname'] = 'Beck/Call'
	elif (td[1].text.strip() == 'Flesh' || td[1].text.strip() == 'Blood'):
		card['cardname'] = 'Flesh/Blood'
	elif (td[1].text.strip() == 'Turn' || td[1].text.strip() == 'Burn'):
		card['cardname'] = 'Turn/Burn'
	elif (td[1].text.strip() == 'Down' || td[1].text.strip() == 'Dirty'):
		card['cardname'] = 'Down/Dirty'
	elif (td[1].text.strip() == 'Give' || td[1].text.strip() == 'Take'):
		card['cardname'] = 'Give/Take'
	elif (td[1].text.strip() == 'Profit' || td[1].text.strip() == 'Loss'):
		card['cardname'] = 'Profit/Loss'
	elif (td[1].text.strip() == 'Protect' || td[1].text.strip() == 'Serve'):
		card['cardname'] = 'Protect/Serve'
	elif (td[1].text.strip() == 'Ready' || td[1].text.strip() == 'Willing'):
		card['cardname'] = 'Ready/Willing'
	elif (td[1].text.strip() == 'Toil' || td[1].text.strip() == 'Trouble'):
		card['cardname'] = 'Toil/Trouble'

	print card
	f.write(card['count'] + ' ' + card['cardname'] + '\n')


def getModernDecks():
	modern_decks = crawlWebPage()

def main():
	'Starting mtggoldfish deck scraper...'
	getModernDecks()

if __name__ == '__main__':
	main()
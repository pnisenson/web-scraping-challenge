hemi_name = ['assfsdfsdfds', 'dfbfdbbfggfb']
hemi_link = ['ass.html', 'dfbf.html']
scraped_data = {}
number = 1
img = 'img' + str(number)
for name in hemi_name:
    for link in hemi_link:
        scraped_data[img] = {name:link}
        hemi_link.remove(link)
        number += 1
        img = 'img' + str(number)

print(scraped_data)
print(scraped_data['img2'].values())

html = 'www.google.com'

new = html.strip("'")
print(html)
print(new)

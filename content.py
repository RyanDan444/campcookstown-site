# Every word and every fact on the site lives here. build.py only renders.
# Rules: no dashes anywhere a customer reads. Real reviews, real photos, real numbers only.
# Positive framing: say what camp is, never what it is not.

SITE = 'https://campcookstown.com'
BOOK_HOST = 'https://book.campcookstown.com'
START = BOOK_HOST + '/get-started'          # the free meet and greet, three short steps
SIGNIN = BOOK_HOST + '/login?signin=1'       # returning families
PRICING_JSON = BOOK_HOST + '/pricing.json'   # live rates from the booking system

PHONE = '(705) 434-4777'
TEL = 'tel:+17054344777'
TEXT_NUMBER = '705 410 2267'                 # the camp texting number (Gracie answers)
SMS = 'sms:+17054102267'
EMAIL = 'info@campcookstown.com'
ADDRESS = '5268 Simcoe County Road 56, Essa, Ontario L0L 1L0'
MAPS = 'https://maps.app.goo.gl/DBmRbvCA1rHMKMPw8'
SOCIAL = [('Instagram', 'https://www.instagram.com/campcookstown/'),
          ('TikTok', 'https://www.tiktok.com/@campcookstown'),
          ('Facebook', 'https://www.facebook.com/pages/Camp-Cookstown/124979261032671'),
          ('YouTube', 'https://www.youtube.com/user/CampCookstownChannel')]
YOUTUBE_ID = 'E3um-9nFE2Q'
RATING = '4.8'
REVIEW_COUNT = '281'
GTM = ''   # Camp's Tag Manager container id, host gated to campcookstown.com

CTA = 'Book a free meet and greet'
CTA_SHORT = 'Free meet and greet'
CTA_SUB = 'Free, about twenty minutes. Then your dog’s first day or night is on us.'

# ---------------------------------------------------------------- photos (slug -> alt). All real.
PHOTOS = {
 'counselor-field-sky':  'A camp counselor laughing on the field with a golden retriever and a yellow lab in her lap, more dogs behind her under a big sky',
 'goldens-asleep':       'Two golden retrievers fast asleep, heads together, on a red blanket',
 'whippet-hoodie':       'A grey whippet wrapped in a fleece, held by a counselor in a Camp Cookstown hoodie',
 'chihuahua-blanket':    'A chihuahua wrapped in a white fleece blanket in the barn',
 'goldens-pink-pool':    'A golden retriever puppy and an adult golden side by side in a pink puppy pool',
 'goldens-two-faces':    'Two golden retrievers, a puppy and an adult, looking straight into the camera on the field',
 'counselor-aussie':     'Taylor, camp manager, laughing as an Australian shepherd licks her cheek in the barn',
 'hannah':               'Hannah, camp manager, smiling in the barn with a cavalier, a chihuahua and a small terrier in her arms',
 'golden-water':         'A soaking wet golden retriever grinning up from the water',
 'cavalier-blanket':     'A black and tan cavalier sitting on a pink blanket against the barn wall',
 'senior-golden-grass':  'A senior golden retriever smiling in tall grass at the edge of the water',
 'dachshund-nap':        'A dachshund asleep upside down on a fluffy bed',
 'spaniel-pool-hat':     'A cavalier in a denim sun hat stepping through a blue puppy pool',
 'lab-and-pal':          'A yellow lab lying in the barn with a small black dog resting on its back',
 'three-goldens-hearts': 'Three golden retrievers posing in front of paper hearts on Valentine’s Day',
 'party-hats':           'Six dogs in party hats lined up in the barn for a birthday',
 'pack-looking-up':      'A dozen dogs in the barn all looking up at the camera at once',
 'frenchies-grass':      'Two French bulldogs on the grass, seen from above',
 'barn-sunset':          'The Camp Cookstown barn at the end of the lane at sunset, fields either side and the sky on fire',
 'barn-lane-pano':       'The black barn and the lane at Camp Cookstown with the fields behind',
 'barn-inside-a':        'Inside the heated barn at Camp Cookstown, wood walls and fresh shavings',
 'barn-inside-b':        'The barn at Camp Cookstown, a wide open room with wood walls and shavings',
 'barn-inside-beds':     'Dog beds on the shavings inside the Camp Cookstown barn',
 'barn-asleep-shavings': 'A pile of dogs asleep together on the shavings in the barn',
 'field-pack-barn':      'The pack out on the green field with the barn behind',
 'field-pack-lane':      'A dozen dogs walking the lane by the barn on a sunny day',
 'field-run':            'Dogs running full tilt across the field at camp',
 'pool-two-dogs':        'Two dogs cooling off in a blue puppy pool',
 'pool-shake':           'A bearded collie shaking off after the puppy pool',
 'aussie-bucket':        'An Australian shepherd puppy with its paws in a water bucket',
 'golden-yawn':          'A golden retriever mid yawn on the shavings',
 'white-dog-roll':       'A white dog rolling on its back in the grass',
 'camp-pano':            'The whole camp seen from the field, the barn in the middle',
 'film-willow':          'The pack lying in the shade under the willow tree',
 'film-nap':             'A bulldog dozing in the wood chips',
 'film-belly':           'A white dog on its back, smiling, getting a belly rub',
 'film-golden':          'A golden retriever pushing its nose right into the camera',
 'film-hose':            'A bulldog leaping into the spray from the hose',
 'film-spa':             'A dog in the spa bath',
}

# ---------------------------------------------------------------- reviews, real, as Google shows them
REVIEWS = [
 ('Meloney Simich', 'Our boy Chip absolutely loves Camp Cookstown. The staff are amazing, and their love for the dogs is obvious. If you are looking for a safe, fun place where your dog can just be a dog, I highly recommend it.'),
 ('Stefanie G', 'Teddy had his first day at camp yesterday and absolutely loved it. He came home happy, calm, and exhausted, a sure sign he had the best time.'),
 ('Debbie Shooter', 'My 13 year old Aussiedoodle has been coming for years and my St. Bernadoodle for almost 9 years. I will go nowhere else for peace of mind.'),
 ('Michelle Simons', 'Very balanced, calm, attentive staff. It was the first time leaving our dog. She came back very happy. We love the daily pictures.'),
 ('Jessica Carvalho', 'Took my two huskies for one night and they absolutely had a blast. This was their first time being boarded and it left us at ease knowing they were with such a loving and caring team.'),
 ('Krista Griffin', 'Liberty has been going to Camp Cookstown since she was a puppy, and she absolutely loves it. Complete peace of mind knowing she is in such loving hands.'),
 ('Christine Lemieux', 'My first time with Charlie for an overnight trial and I know he absolutely loved it. Taylor made me feel at ease dropping him off, and it was great to see the stories on Instagram of Charlie enjoying playtime.'),
 ('Stephanie M', 'Puppy Tessa Bear had an amazing time playing with other friendly dogs, and she got a lovely bath before she came home. I love how we got to watch her play on Instagram stories.'),
 ('gbeke tuyo', 'Mazzi stayed for one night and came home happy, energized, and clearly well cared for. It was obvious they genuinely care about the dogs they look after.'),
 ('Ruth Carrasquero', 'Our pups Aquiles and Athena love being part of the larger groups outdoors. The staff is skilled and very detail oriented, and the pick up and drop off process is efficient and safe.'),
]

# ---------------------------------------------------------------- questions
GENERAL_FAQ = [
 ("What does my dog need before the first visit?", "Over three months old, healthy, free of fleas and ticks, and spayed or neutered if over nine months. Then a free meet and greet so we can introduce them to a few campers at a time."),
 ("What is the meet and greet?", "A short first visit, about twenty minutes. You walk the property and meet the team while your dog meets a few new friends in the barn. It is free, and so is their first day or night, one free visit per new camper."),
 ("When can I drop off and pick up?", "Drop off between 7:30 and 8:30 am or 11 am and noon. Pick up between 11 am and noon or 5 and 6 pm. We are open every day of the year."),
 ("Can I cancel?", "Yes, any time, and it costs nothing. Holidays and long weekends take a 50 percent deposit at booking."),
 ("How many dogs are at camp?", "Camp is capped at 40 dogs, in groups matched by size and energy, with counselors beside them from morning to lights out."),
 ("Can I check in on my dog?", "Call or text any time, day or night. Most days there are new photos and stories on Instagram too."),
 ("Is someone with the dogs at night?", "The barn is theirs at night, warm in winter and cool in summer, and a counselor is on the property every night of the year."),
 ("What if my dog gets hurt or sick?", "Every counselor is certified in Pet First Aid and Pet CPR, and a 24 hour emergency vet clinic is close by. A vet visit is $40 plus the clinic’s bill."),
 ("Can you give medication?", "Yes, at no charge. Bring it in the original container with the instructions."),
 ("What about food?", "Bring their usual food and we serve it exactly as you would, one dog at a time so nobody shares. Forgot it? We have food for $50 plus the cost of the bag."),
 ("My dog is a senior. Is camp too much?", "Not at all. Counselors match groups by energy and keep an eye on the slower campers, and there is always a quiet spot in the barn for a nap."),
 ("What if my dog does not get along with another camper?", "Every dog is assessed before joining, and counselors are trained to prevent conflicts and bullying before they start."),
 ("Can I bring a blanket?", "Of course. Just do not expect it home in one piece."),
 ("How far ahead should I book?", "As early as you can. Camp fills up, especially long weekends, March Break and Christmas."),
]
DAY_FAQ = [GENERAL_FAQ[0], GENERAL_FAQ[1], GENERAL_FAQ[2], GENERAL_FAQ[4], GENERAL_FAQ[5], GENERAL_FAQ[3]]
NIGHT_FAQ = [GENERAL_FAQ[6], GENERAL_FAQ[9], GENERAL_FAQ[8], GENERAL_FAQ[7], GENERAL_FAQ[10], GENERAL_FAQ[13]]

# ---------------------------------------------------------------- the day, for the film captions and the clock
# (slot, time label, headline, line, photo). The clock picks the slot by Ontario time.
DAY = [
 ('dropoff',  '7:30 to 8:30 am', 'Drop off',           'Straight out to the field with their friends.', 'counselor-field-sky'),
 ('morning',  'Morning',         'The big romp',       '45 fenced acres of sun, shade and room to run until the zoomies run out.', 'field-run'),
 ('midday',   'Midday',          'Pools and shade',    'Puppy pools when it is hot, sunny spots when it is not.', 'spaniel-pool-hat'),
 ('afternoon','Afternoon',       'Barn naps',          'Heated in winter, cooled in summer. They nap wherever they like.', 'dachshund-nap'),
 ('evening',  'Evening',         'Dinner, one at a time', 'Your food, your portions, served one dog at a time.', 'chihuahua-blanket'),
 ('night',    'Night',           'Lights out with the pack', 'Snuggled in the barn, and a counselor is on the property every night.', 'goldens-asleep'),
]
# Film captions, shown as the footage scrubs. (start fraction, end fraction, small, big)
FILM_CAPTIONS = [
 (0.00, 0.30, 'Morning',   'Straight out to the field with friends.'),
 (0.30, 0.56, 'All day',   'Outside in the sun, the shade and the puppy pools.'),
 (0.56, 0.80, 'Any time',  'Belly rubs whenever they ask.'),
 (0.80, 1.00, 'Afternoon', 'Then a very good nap.'),
]

# ---------------------------------------------------------------- rates (fallbacks; the live figures come from pricing.json)
RATES = {
 'day.week': '50', 'day.pack': '400',
 'overnight.week': '65', 'overnight.weekend': '80', 'overnight.t3': '64', 'overnight.t4': '62', 'overnight.t5': '59',
 'overnight.holiday': '100', 'overnight.pm-pickup': '50',
}

# ---------------------------------------------------------------- the Gracie line
GRACIE_EYEBROW = 'Questions? Any hour.'
GRACIE_H2 = 'Call or text. Gracie answers, day or night.'
GRACIE_P1 = 'Gracie is our front desk, and she is an AI. She answers in seconds, day or night. Ask her what to pack, how a first night goes, or whether there is room this weekend, and she can book your free meet and greet while you are on the line.'
GRACIE_P2 = 'Talk to her the way you would talk to us, in your own words. When a question needs a person, Taylor and Hannah get right back to you.'

# ---------------------------------------------------------------- towns for the landing pages
# slug -> (title, meta description, H1 line one, H1 accent, hero lede, drive line, kind)
# kind: 'boarding' | 'daycare' | 'kennel' | 'camp' | 'puppy' | 'offer-night' | 'offer-day'
TOWNS = {
 'dog-boarding':            ('Dog Boarding near Barrie on 45 Acres | Camp Cookstown', 'Cage free dog boarding at Cookstown, minutes off Highway 400. Days in the field, nights in a heated barn, a counselor on the property every night. From $65 a night, first night free.', 'Dog boarding,', 'the camp way.', 'Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'Minutes off Highway 400 by the Tanger Outlets at Cookstown, an easy drive from Barrie, Innisfil, Alliston, Bradford and Newmarket.', 'boarding'),
 'dog-daycare':             ('Dog Daycare near Barrie and Innisfil | Camp Cookstown', 'Cage free dog day camp on 45 acres at Cookstown. $50 a day, ten day pack $400, first day free. Open every day.', 'Dog daycare', 'on a real farm.', 'A whole day outside on 45 fenced acres with a pack of friends and counselors who adore them.', 'Minutes from Highway 400 at Cookstown, an easy drive from Barrie, Innisfil, Alliston and Bradford.', 'daycare'),
 'dog-boarding-barrie':     ('Dog Boarding Barrie | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Barrie families, 25 minutes down the 400 at Cookstown. Days in the field, nights in a heated barn, from $65 a night. First night free.', 'Dog boarding for', 'Barrie families.', 'About 25 minutes from Barrie. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'Straight down Highway 400 to Cookstown, by the Tanger Outlets. About 25 minutes from Barrie.', 'boarding'),
 'dog-daycare-barrie':      ('Dog Daycare Barrie | Day Camp on 45 Acres | Camp Cookstown', 'Dog daycare for Barrie families, 25 minutes down the 400 at Cookstown. A whole day outside with the pack, $50 a day, first day free.', 'Dog daycare for', 'Barrie families.', 'About 25 minutes from Barrie. A whole day outside on 45 fenced acres with a pack of friends.', 'Straight down Highway 400 to Cookstown, by the Tanger Outlets. About 25 minutes from Barrie.', 'daycare'),
 'dog-camp':                ('Dog Camp near Barrie | Camp Cookstown, Cookstown Ontario', 'A real camp for dogs on 45 acres at Cookstown. Day camp and overnight camp, a heated barn, puppy pools and fields. Since 2008.', 'A real camp', 'for dogs.', 'Forty five acres of fields, a heated barn, puppy pools and a pack of friends. Day camp and sleepovers, since 2008.', 'Minutes off Highway 400 by the Tanger Outlets at Cookstown, an easy drive from Barrie, Innisfil, Alliston, Bradford and Newmarket.', 'camp'),
 '1-free-night':            ('First Night Free | Dog Boarding at Camp Cookstown', 'New campers get their first night free at Camp Cookstown. Cage free dog boarding on 45 acres at Cookstown, a heated barn and a counselor on the property every night.', 'Your dog’s first', 'night is on us.', 'Come for a free meet and greet, then your dog’s first night at camp is free. Days in the field, nights in the heated barn with the pack.', 'Minutes off Highway 400 by the Tanger Outlets at Cookstown, an easy drive from Barrie, Innisfil, Alliston, Bradford and Newmarket.', 'offer-night'),
 '2-free-days':             ('First Day Free | Dog Daycare at Camp Cookstown', 'New campers get their first day free at Camp Cookstown. Cage free dog day camp on 45 acres at Cookstown, minutes off Highway 400.', 'Your dog’s first', 'day is on us.', 'Come for a free meet and greet, then your dog’s first day at camp is free. A whole day outside with the pack.', 'Minutes off Highway 400 by the Tanger Outlets at Cookstown, an easy drive from Barrie, Innisfil, Alliston, Bradford and Newmarket.', 'offer-day'),
 'dog-boarding-newmarket':  ('Dog Boarding Newmarket | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Newmarket families, 35 minutes up the 400 at Cookstown. Days in the field, nights in a heated barn, from $65 a night. First night free.', 'Dog boarding for', 'Newmarket families.', 'About 35 minutes from Newmarket. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'Up Highway 400 to Cookstown. About 35 minutes from Newmarket, Aurora and East Gwillimbury.', 'boarding'),
 'dog-boarding-innisfil':   ('Dog Boarding Innisfil | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Innisfil families, about 25 minutes from Alcona and Lefroy to camp at Cookstown. Days in the field, nights in a heated barn. First night free.', 'Dog boarding for', 'Innisfil families.', 'About 25 minutes from Alcona and Lefroy. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'About 25 minutes from Alcona, Lefroy and Stroud.', 'boarding'),
 'dog-boarding-alliston':   ('Dog Boarding Alliston | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Alliston families, about 18 minutes to camp at Cookstown. Days in the field, nights in a heated barn. First night free.', 'Dog boarding for', 'Alliston families.', 'About 18 minutes from Alliston. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'About 18 minutes from Alliston, 21 from Beeton and 30 from Tottenham.', 'boarding'),
 'dog-boarding-borden':     ('Dog Boarding near CFB Borden | Camp Cookstown', 'Dog boarding for Borden and Angus families, about 30 minutes to camp at Cookstown. Days in the field, nights in a heated barn. Long stays welcome.', 'Dog boarding for', 'Borden families.', 'Deployments, courses and postings: long stays are welcome, and the night rate drops the longer your dog stays. Days on 45 acres, nights in a heated barn with the pack.', 'About 30 minutes from CFB Borden and Angus.', 'boarding'),
 'dog-kennel-barrie':       ('Dog Kennel Barrie | The Camp Version | Camp Cookstown', 'Searching for a dog kennel in Barrie? Camp Cookstown is the cage free version, 25 minutes down the 400. Days in the field, nights in a heated barn, from $65 a night.', 'Dog kennel', 'near Barrie?', 'Here is the camp version. Days on 45 acres with the pack, nights in a heated barn, and a counselor on the property every night.', 'Straight down Highway 400 to Cookstown, by the Tanger Outlets. About 25 minutes from Barrie.', 'kennel'),
 'dog-kennel':              ('Dog Kennel near Me | The Camp Version | Camp Cookstown', 'Searching for a dog kennel? Camp Cookstown is the cage free version at Cookstown, minutes off Highway 400. Days in the field, nights in a heated barn, from $65 a night.', 'Looking for a', 'dog kennel?', 'Here is the camp version. Days on 45 acres with the pack, nights in a heated barn, and a counselor on the property every night.', 'Minutes off Highway 400 by the Tanger Outlets at Cookstown, an easy drive from Barrie, Innisfil, Alliston, Bradford and Newmarket.', 'kennel'),
 'puppy-camp':              ('Puppy Camp and Puppy Daycare near Barrie | Camp Cookstown', 'Puppy day camp and boarding on 45 acres at Cookstown. Small matched groups, gentle introductions, from three months old. First day free.', 'Puppy camp,', 'gently.', 'From three months old. Small groups matched by size and energy, gentle introductions, and counselors beside them all day.', 'Minutes off Highway 400 by the Tanger Outlets at Cookstown, an easy drive from Barrie, Innisfil, Alliston, Bradford and Newmarket.', 'puppy'),
 'dog-daycare-innisfil':    ('Dog Daycare Innisfil | Day Camp on 45 Acres | Camp Cookstown', 'Dog daycare for Innisfil families, about 25 minutes from Alcona and Lefroy to camp at Cookstown. A whole day outside with the pack. First day free.', 'Dog daycare for', 'Innisfil families.', 'About 25 minutes from Alcona and Lefroy. A whole day outside on 45 fenced acres with a pack of friends.', 'About 25 minutes from Alcona, Lefroy and Stroud.', 'daycare'),
 'dog-boarding-bradford':   ('Dog Boarding Bradford | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Bradford families, about 23 minutes to camp at Cookstown. Days in the field, nights in a heated barn. First night free.', 'Dog boarding for', 'Bradford families.', 'About 23 minutes from Bradford. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'About 23 minutes from Bradford and Bond Head.', 'boarding'),
 'dog-boarding-aurora':     ('Dog Boarding Aurora | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Aurora families, 40 minutes up the 400 at Cookstown. Days in the field, nights in a heated barn, from $65 a night. First night free.', 'Dog boarding for', 'Aurora families.', 'About 40 minutes from Aurora. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'Up Highway 400 to Cookstown. About 40 minutes from Aurora.', 'boarding'),
 'dog-boarding-vaughan':    ('Dog Boarding Vaughan | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Vaughan, Woodbridge and Kleinburg families, about 45 minutes up the 400 at Cookstown. Days in the field, nights in a heated barn, from $65 a night.', 'Dog boarding for', 'Vaughan families.', 'About 45 minutes from Vaughan. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'Up Highway 400 to Cookstown. About 45 minutes from Vaughan, Woodbridge, Maple and Kleinburg.', 'boarding'),
 'dog-boarding-caledon':    ('Dog Boarding Caledon | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for Caledon and Bolton families, about 50 minutes to camp at Cookstown. Days in the field, nights in a heated barn. First night free.', 'Dog boarding for', 'Caledon families.', 'About 50 minutes from Caledon. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'About 45 minutes from Palgrave, 47 from Bolton and 52 from Caledon East.', 'boarding'),
 'dog-boarding-king-city':  ('Dog Boarding King City | Cage Free Camp on 45 Acres | Camp Cookstown', 'Dog boarding for King City, Schomberg and Nobleton families, about 35 minutes up the 400 at Cookstown. Days in the field, nights in a heated barn, from $65 a night.', 'Dog boarding for', 'King City families.', 'About 35 minutes from King City. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'Up Highway 400 to Cookstown. About 35 minutes from King City, 25 from Schomberg and 35 from Nobleton.', 'boarding'),
 'dog-boarding-east-gwillimbury': ('Dog Boarding East Gwillimbury | Camp Cookstown', 'Dog boarding for East Gwillimbury, Holland Landing and Sharon families, about 32 minutes to camp at Cookstown. Days in the field, nights in a heated barn. First night free.', 'Dog boarding for', 'East Gwillimbury.', 'About 32 minutes from East Gwillimbury. Days on 45 acres, nights in a heated barn with the pack, and a counselor on the property every night.', 'About 32 minutes from Holland Landing, Sharon, Queensville and Mount Albert.', 'boarding'),
}

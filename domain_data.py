# Domain data for "Tên miền dễ thương" game
import random

# List of 1000 legitimate, safe domains
LEGITIMATE_DOMAINS = [
    "google.com", "facebook.com", "youtube.com", "wikipedia.org", "amazon.com",
    "microsoft.com", "apple.com", "linkedin.com", "twitter.com", "instagram.com",
    "reddit.com", "netflix.com", "tiktok.com", "discord.com", "spotify.com",
    "github.com", "stackoverflow.com", "zoom.us", "dropbox.com", "adobe.com",
    "salesforce.com", "oracle.com", "ibm.com", "intel.com", "nvidia.com",
    "samsung.com", "sony.com", "lg.com", "canon.com", "nikon.com",
    "booking.com", "airbnb.com", "uber.com", "lyft.com", "paypal.com",
    "visa.com", "mastercard.com", "americanexpress.com", "chase.com", "bankofamerica.com",
    "wellsfargo.com", "citibank.com", "hsbc.com", "jpmorgan.com", "goldmansachs.com",
    "cnn.com", "bbc.com", "reuters.com", "bloomberg.com", "wsj.com",
    "nytimes.com", "theguardian.com", "forbes.com", "techcrunch.com", "wired.com",
    "espn.com", "nfl.com", "nba.com", "fifa.com", "olympic.org",
    "weather.com", "accuweather.com", "nationalgeographic.com", "discovery.com", "history.com",
    "harvard.edu", "mit.edu", "stanford.edu", "berkeley.edu", "caltech.edu",
    "oxford.ac.uk", "cambridge.ac.uk", "imperial.ac.uk", "ethz.ch", "epfl.ch",
    "nus.edu.sg", "ntu.edu.sg", "hku.hk", "ust.hk", "cuhk.edu.hk",
    "utm.my", "usm.my", "upm.edu.my", "ukm.my", "um.edu.my",
    "ui.ac.id", "itb.ac.id", "ugm.ac.id", "its.ac.id", "unpad.ac.id",
    "chula.ac.th", "mahidol.ac.th", "ku.ac.th", "mut.ac.th", "kmutt.ac.th",
    "nus.edu", "ntu.edu", "smu.edu.sg", "sit.edu.sg", "sutd.edu.sg",
    "hust.edu.vn", "vnu.edu.vn", "uit.edu.vn", "hcmus.edu.vn", "bku.edu.vn",
    "mcdonalds.com", "starbucks.com", "kfc.com", "subway.com", "pizzahut.com",
    "dominos.com", "burgerking.com", "tacobell.com", "chipotle.com", "dunkindonuts.com",
    "walmart.com", "target.com", "costco.com", "homedepot.com", "lowes.com",
    "bestbuy.com", "macys.com", "nordstrom.com", "gap.com", "hm.com",
    "nike.com", "adidas.com", "puma.com", "underarmour.com", "reebok.com",
    "levis.com", "calvinklein.com", "tommyhilfiger.com", "ralphlauren.com", "gucci.com",
    "louisvuitton.com", "chanel.com", "prada.com", "hermes.com", "rolex.com",
    "toyota.com", "honda.com", "ford.com", "chevrolet.com", "bmw.com",
    "mercedes.com", "audi.com", "volkswagen.com", "nissan.com", "mazda.com",
    "hyundai.com", "kia.com", "lexus.com", "infiniti.com", "acura.com",
    "tesla.com", "spacex.com", "boeing.com", "airbus.com", "ge.com",
    "siemens.com", "philips.com", "panasonic.com", "toshiba.com", "hitachi.com",
    "mitsubishi.com", "fujitsu.com", "nec.com", "sharp.com", "ricoh.com",
    "cisco.com", "vmware.com", "dell.com", "hp.com", "lenovo.com",
    "asus.com", "acer.com", "msi.com", "gigabyte.com", "asrock.com",
    "mongodb.com", "mysql.com", "postgresql.org", "redis.io", "elasticsearch.co",
    "docker.com", "kubernetes.io", "jenkins.io", "gitlab.com", "bitbucket.org",
    "atlassian.com", "jira.com", "confluence.com", "slack.com", "teams.microsoft.com",
    "telegram.org", "whatsapp.com", "viber.com", "line.me", "wechat.com",
    "skype.com", "facetime.apple.com", "googlemeet.com", "webex.com", "gotomeeting.com",
    "mozilla.org", "firefox.com", "chrome.google.com", "safari.apple.com", "edge.microsoft.com",
    "opera.com", "brave.com", "tor.org", "duckduckgo.com", "bing.com",
    "yahoo.com", "yandex.com", "baidu.com", "ask.com", "aol.com",
    "gmail.com", "outlook.com", "icloud.com", "protonmail.com", "tutanota.com",
    "mailchimp.com", "constantcontact.com", "sendgrid.com", "mailgun.com", "postmark.com",
    "shopify.com", "woocommerce.com", "magento.com", "bigcommerce.com", "squarespace.com",
    "wix.com", "weebly.com", "godaddy.com", "namecheap.com", "bluehost.com",
    "hostgator.com", "siteground.com", "dreamhost.com", "inmotionhosting.com", "a2hosting.com",
    "cloudflare.com", "aws.amazon.com", "azure.microsoft.com", "cloud.google.com", "digitalocean.com",
    "linode.com", "vultr.com", "heroku.com", "netlify.com", "vercel.com",
    "wordpress.com", "drupal.org", "joomla.org", "typo3.org", "ghost.org",
    "medium.com", "substack.com", "blogger.com", "tumblr.com", "pinterest.com",
    "behance.net", "dribbble.com", "deviantart.com", "flickr.com", "500px.com",
    "unsplash.com", "pexels.com", "shutterstock.com", "getty.com", "istockphoto.com",
    "canva.com", "figma.com", "sketch.com", "invision.com", "zeplin.io",
    "framer.com", "principle.design", "protopie.io", "axure.com", "balsamiq.com",
    "trello.com", "asana.com", "notion.so", "airtable.com", "monday.com",
    "basecamp.com", "todoist.com", "evernote.com", "onenote.com", "googledocs.com",
    "office365.com", "onedrive.com", "googledrive.com", "box.com", "sync.com",
    "pcloud.com", "mega.nz", "mediafire.com", "4shared.com", "rapidshare.com",
    "wetransfer.com", "sendspace.com", "zippyshare.com", "uploaded.net", "filehosting.org",
    "upwork.com", "freelancer.com", "fiverr.com", "99designs.com", "toptal.com",
    "indeed.com", "glassdoor.com", "monster.com", "careerbuilder.com", "ziprecruiter.com",
    "coursera.org", "edx.org", "udemy.com", "khanacademy.org", "codecademy.com",
    "pluralsight.com", "lynda.com", "skillshare.com", "masterclass.com", "brilliant.org",
    "duolingo.com", "babbel.com", "rosettastone.com", "memrise.com", "busuu.com",
    "tripadvisor.com", "expedia.com", "hotels.com", "priceline.com", "kayak.com",
    "skyscanner.com", "momondo.com", "cheapflights.com", "orbitz.com", "travelocity.com",
    "yelp.com", "zomato.com", "opentable.com", "grubhub.com", "doordash.com",
    "ubereats.com", "postmates.com", "seamless.com", "deliveroo.com", "foodpanda.com",
    "grab.com", "gojek.com", "didi.com", "ola.com", "99.co",
    "zillow.com", "realtor.com", "trulia.com", "redfin.com", "apartments.com",
    "rent.com", "padmapper.com", "hotpads.com", "zumper.com", "rentals.com",
    "craigslist.org", "ebay.com", "etsy.com", "alibaba.com", "aliexpress.com",
    "wish.com", "overstock.com", "wayfair.com", "ikea.com", "houzz.com",
    "pinterest.com", "homedepot.com", "lowes.com", "menards.com", "acehardware.com",
    "sephora.com", "ulta.com", "maccosmetics.com", "lorealparis.com", "maybelline.com",
    "covergirl.com", "revlon.com", "estee-lauder.com", "clinique.com", "lancome.com",
    "zara.com", "hm.com", "uniqlo.com", "forever21.com", "urbanoutfitters.com",
    "anthropologie.com", "freepeople.com", "jcrew.com", "bananarepublic.com", "oldnavy.com",
    "victoriassecret.com", "bathandbodyworks.com", "saks.com", "neimanmarcus.com", "bergdorfs.com",
    "tiffany.com", "cartier.com", "bulgari.com", "chopard.com", "vancleefarpels.com",
    "patek.com", "audemars-piguet.com", "vacheron-constantin.com", "jaeger-lecoultre.com", "iwc.com",
    "omega.com", "tagheuer.com", "breitling.com", "tudor.com", "seiko.com",
    "citizen.com", "casio.com", "gshock.com", "timex.com", "fossil.com",
    "swatch.com", "tissot.com", "hamilton.com", "longines.com", "mido.com",
    "oris.com", "frederique-constant.com", "montblanc.com", "movado.com", "baume-mercier.com",
    "glashutte.com", "a-lange-soehne.com", "richard-mille.com", "franck-muller.com", "urwerk.com",
    "mbandm.com", "jomashop.com", "chrono24.com", "tourneau.com", "watchstation.com",
    "ashford.com", "crown-golay.com", "hodinkee.com", "watchtime.com", "ablogtowatch.com",
    "monochrome-watches.com", "fratellowatches.com", "deployant.com", "revolution.watch", "timeandtidewatches.com",
    "wornandwound.com", "watchesbysjx.com", "escapementmagazine.com", "watchpro.com", "jewelry-news-network.com",
    "robbereport.com", "luxurydaily.com", "jckonline.com", "professionaljeweler.com", "nationalwjeweler.com",
    "diamonds.net", "idexonline.com", "rough-polished.com", "gemguide.com", "pricescope.com",
    "bluenile.com", "jamesallen.com", "brilliantearth.com", "ritani.com", "whiteflash.com",
    "gia.edu", "guebelin.com", "ssef.ch", "ags.org", "egl.co.za",
    "instagram.com", "facebook.com", "twitter.com", "linkedin.com", "tiktok.com",
    "snapchat.com", "telegram.org", "whatsapp.com", "messenger.com", "discord.com",
    "reddit.com", "quora.com", "stackoverflow.com", "github.com", "gitlab.com",
    "bitbucket.org", "sourceforge.net", "codepen.io", "jsfiddle.net", "replit.com",
    "codesandbox.io", "glitch.com", "heroku.com", "netlify.com", "vercel.com",
    "firebase.google.com", "supabase.io", "planetscale.com", "railway.app", "fly.io",
    "render.com", "deno.com", "bun.sh", "node.js.org", "python.org",
    "ruby-lang.org", "php.net", "java.com", "golang.org", "rust-lang.org",
    "swift.org", "kotlinlang.org", "scala-lang.org", "clojure.org", "erlang.org",
    "elixir-lang.org", "haskell.org", "ocaml.org", "fsharp.org", "dart.dev",
    "flutter.dev", "reactjs.org", "vuejs.org", "angular.io", "svelte.dev",
    "nextjs.org", "nuxtjs.org", "gatsbyjs.com", "astro.build", "remix.run",
    "solidjs.com", "preactjs.com", "lit.dev", "stenciljs.com", "alpinejs.dev",
    "htmx.org", "hyperscript.org", "stimulus.hotwired.dev", "turbo.hotwired.dev", "inertiajs.com",
    "laravel.com", "symfony.com", "codeigniter.com", "cakephp.org", "yiiframework.com",
    "zendframework.com", "phalcon.io", "slim-framework.com", "lumen.laravel.com", "api-platform.com",
    "django.com", "flask.palletsprojects.com", "fastapi.tiangolo.com", "tornado.com", "pyramid.trypyramid.com",
    "bottle.py", "cherrypy.org", "web2py.com", "turbogears.org", "pylons.org",
    "expressjs.com", "koajs.com", "fastify.io", "nestjs.com", "adonisjs.com",
    "meteorjs.com", "sails.js.org", "hapijs.com", "restify.com", "totaljs.com",
    "rails.org", "sinatra.rb", "hanami.rb", "roda.rb", "cuba.is",
    "padrino.rb", "grape.rb", "dry-rb.org", "rom-rb.org", "sequel.rb",
    "spring.io", "dropwizard.io", "micronaut.io", "quarkus.io", "helidon.io",
    "sparkjava.com", "javalin.io", "ratpack.io", "vert-x.io", "playframework.com",
    "struts.apache.org", "wicket.apache.org", "tapestry.apache.org", "jsf.java.net", "grails.org",
    "dotnet.microsoft.com", "asp.net", "nancyfx.org", "servicestack.net", "umbraco.com",
    "sitefinity.com", "kentico.com", "episerver.com", "orchard.net", "dotnetnuke.com",
    "wordpress.org", "drupal.org", "joomla.org", "typo3.org", "modx.com",
    "concrete5.org", "silverstripe.org", "october.cms", "craft.cms", "statamic.com",
    "kirby.cms", "processwire.com", "grav.getgrav.org", "bolt.cm", "pico.cms",
    "ghost.org", "jekyll.rb", "hugo.io", "gatsby.js.org", "11ty.dev",
    "gridsome.org", "scully.io", "vuepress.vuejs.org", "docusaurus.io", "gitbook.com",
    "notion.so", "obsidian.md", "roam.research", "logseq.com", "zettlr.com",
    "typora.io", "mark.text", "vnote.fun", "notable.app", "bear.app",
    "ulysses.app", "ia.writer", "scapple.com", "scrivener.com", "writeroom.com",
    "focused.app", "draft.app", "hemingway.app", "grammarly.com", "linguix.com",
    "prowritingaid.com", "autocrit.com", "readable.com", "nitpicker.com", "whitesmoke.com",
    "ginger.com", "paperrater.com", "essaybot.com", "perfectit.com", "slickwrite.com",
    "after-the-deadline.com", "textgears.com", "reverso.net", "deepl.com", "translate.google.com",
    "microsoft.com/translator", "yandex.com/translate", "systran.net", "linguee.com", "wordreference.com",
    "collinsdictionary.com", "merriam-webster.com", "dictionary.cambridge.org", "oxforddictionaries.com", "macmillandictionary.com",
    "thefreedictionary.com", "vocabulary.com", "thesaurus.com", "rhymezone.com", "onelook.com",
    "etymonline.com", "urbandictionary.com", "acronymfinder.com", "abbreviations.com", "yourdictionary.com",
    "investopedia.com", "morningstar.com", "bloomberg.com", "marketwatch.com", "fool.com",
    "seekingalpha.com", "zacks.com", "gurufocus.com", "finviz.com", "tradingview.com",
    "yahoo.finance.com", "google.finance.com", "msn.money.com", "cnn.money.com", "cnbc.com",
    "reuters.com", "ft.com", "wsj.com", "economist.com", "barrons.com",
    "forbes.com", "fortune.com", "businessinsider.com", "fastcompany.com", "inc.com",
    "entrepreneur.com", "harvard.business.review.com", "mckinsey.com", "bcg.com", "bain.com",
    "accenture.com", "deloitte.com", "pwc.com", "ey.com", "kpmg.com",
    "reddit.com/r/investing", "reddit.com/r/stocks", "reddit.com/r/financialindependence", "reddit.com/r/personalfinance", "reddit.com/r/SecurityAnalysis",
    "reddit.com/r/ValueInvesting", "reddit.com/r/dividends", "reddit.com/r/ETFs", "reddit.com/r/SecurityAnalysis", "reddit.com/r/financialplanning",
    "bogleheads.org", "morningstar.ca", "fool.ca", "globeandmail.com", "financialpost.com",
    "moneysense.ca", "ratehub.ca", "savvynewcanadians.com", "youngandthrifty.ca", "milliondollarjourney.com",
    "canadiancouchpotato.com", "maplemoneycom", "canadianfinanceblog.com", "lowestrates.ca", "greedyrates.ca"
]

# List of suspicious/scam-like domains
SUSPICIOUS_DOMAINS = [
    # Typosquatting of major brands
    "gooogle.com", "facebok.com", "youtuube.com", "amazom.com", "micorsoft.com",
    "appple.com", "linkdin.com", "twiter.com", "instgram.com", "redit.com",
    "netflx.com", "tiktak.com", "discrd.com", "spotfy.com", "githib.com",
    "stackoverfow.com", "zoon.us", "dropbx.com", "adbe.com", "salesforse.com",
    
    # Suspicious domain patterns
    "secure-banking-update.com", "verify-paypal-account.net", "amazon-security-alert.org",
    "microsoft-support-team.info", "apple-id-verification.biz", "google-account-suspended.co",
    "facebook-security-check.us", "twitter-account-locked.tk", "instagram-verify-now.ml",
    "linkedin-premium-offer.ga", "netflix-free-trial.cf", "spotify-premium-free.tk",
    
    # Banking/Financial scams
    "bank-account-verification.com", "credit-score-free.net", "loan-approved-instantly.org",
    "tax-refund-pending.info", "irs-refund-claim.biz", "stimulus-payment-ready.co",
    "cryptocurrency-investment.us", "bitcoin-doubler.tk", "ethereum-giveaway.ml",
    "forex-trading-signals.ga", "binary-options-profit.cf", "crypto-mining-pool.tk",
    
    # Tech support scams
    "windows-security-warning.com", "computer-virus-detected.net", "pc-cleanup-required.org",
    "antivirus-expired-renew.info", "system-error-fix-now.biz", "malware-removal-service.co",
    "tech-support-microsoft.us", "apple-support-call.tk", "google-chrome-update.ml",
    "firefox-security-patch.ga", "adobe-flash-update.cf", "java-urgent-update.tk",
    
    # Shopping/Prize scams
    "winner-notification.com", "congratulations-selected.net", "prize-claim-center.org",
    "amazon-gift-card-free.info", "iphone-giveaway-real.biz", "survey-reward-cash.co",
    "product-tester-needed.us", "exclusive-deal-today.tk", "limited-time-offer.ml",
    "discount-coupon-code.ga", "cashback-guarantee.cf", "refund-processing.tk",
    
    # Romance/Dating scams
    "lonely-hearts-connect.com", "find-true-love-now.net", "dating-millionaire.org",
    "beautiful-singles-area.info", "meet-lonely-wife.biz", "discreet-affair-site.co",
    "sugar-daddy-finder.us", "international-dating.tk", "mail-order-bride.ml",
    "romance-overseas.ga", "love-connection-real.cf", "soulmate-waiting.tk",
    
    # Suspicious TLDs with common words
    "free-download.tk", "best-offer.ml", "urgent-update.ga", "secure-login.cf",
    "verify-account.tk", "claim-reward.ml", "download-now.ga", "instant-access.cf",
    "limited-offer.tk", "exclusive-deal.ml", "special-promotion.ga", "member-only.cf",
    
    # Fake news/clickbait
    "breaking-news-alert.com", "shocking-discovery.net", "celebrity-scandal.org",
    "government-secret.info", "conspiracy-revealed.biz", "miracle-cure-found.co",
    "doctors-hate-this.us", "weight-loss-secret.tk", "anti-aging-discovery.ml",
    "cancer-cure-hidden.ga", "pharmaceutical-scam.cf", "natural-remedy-works.tk",
    
    # Cryptocurrency scams
    "bitcoin-investment-bot.com", "crypto-trading-robot.net", "ethereum-mining-profit.org",
    "blockchain-opportunity.info", "ico-presale-bonus.biz", "defi-yield-farming.co",
    "nft-minting-early.us", "altcoin-moonshot.tk", "crypto-signals-vip.ml",
    "bitcoin-ATM-locator.ga", "coinbase-support-help.cf", "binance-verification.tk",
    
    # Fake services
    "essay-writing-cheap.com", "fake-id-maker.net", "diploma-online-fast.org",
    "credit-repair-instant.info", "background-check-free.biz", "people-search-unlimited.co",
    "reverse-phone-lookup.us", "email-address-finder.tk", "social-media-hack.ml",
    "password-recovery-tool.ga", "account-hacking-service.cf", "spy-software-mobile.tk",
    
    # Phishing variations
    "paypal-security.com", "amazon-customer.net", "microsoft-office.org",
    "apple-icloud.info", "google-gmail.biz", "facebook-meta.co",
    "twitter-x.us", "instagram-meta.tk", "linkedin-corp.ml",
    "netflix-streaming.ga", "spotify-music.cf", "youtube-google.tk",
    
    # Government impersonation
    "irs-tax-office.com", "social-security-admin.net", "department-treasury.org",
    "immigration-services.info", "court-summons.biz", "police-department.co",
    "fbi-investigation.us", "homeland-security.tk", "customs-border.ml",
    "postal-service.ga", "motor-vehicle.cf", "unemployment-benefits.tk",
    
    # Health scams
    "covid-vaccine-free.com", "weight-loss-pill.net", "male-enhancement.org",
    "anti-aging-cream.info", "memory-supplement.biz", "pain-relief-natural.co",
    "diabetes-cure.us", "cancer-treatment.tk", "hair-growth-formula.ml",
    "vision-improvement.ga", "hearing-aid-free.cf", "dental-implants-cheap.tk",
    
    # Investment scams
    "stock-picks-guaranteed.com", "forex-signals-winning.net", "binary-options-strategy.org",
    "real-estate-flip.info", "precious-metals-dealer.biz", "commodity-trading.co",
    "hedge-fund-access.us", "private-equity-invest.tk", "venture-capital-opportunity.ml",
    "oil-gas-investment.ga", "solar-energy-stocks.cf", "marijuana-stocks-boom.tk",
    
    # Travel scams
    "vacation-package-deal.com", "cruise-discount.net", "airline-tickets-cheap.org",
    "hotel-booking-discount.info", "timeshare-resale.biz", "travel-insurance-claim.co",
    "visa-application-fast.us", "passport-renewal-express.tk", "immigration-lawyer.ml",
    "green-card-lottery.ga", "work-visa-guaranteed.cf", "student-visa-approval.tk",
    
    # Employment scams
    "work-from-home-easy.com", "make-money-online.net", "part-time-income.org",
    "data-entry-jobs.info", "envelope-stuffing-work.biz", "survey-taking-paid.co",
    "mystery-shopping-jobs.us", "customer-service-remote.tk", "virtual-assistant-hire.ml",
    "freelance-writing-gigs.ga", "translation-jobs-online.cf", "tutoring-opportunity.tk",
    
    # Charity scams
    "disaster-relief-fund.com", "children-charity-help.net", "cancer-research-donate.org",
    "veterans-assistance.info", "animal-rescue-save.biz", "homeless-shelter-support.co",
    "education-fund-donate.us", "medical-expenses-help.tk", "emergency-aid-fund.ml",
    "religious-mission-support.ga", "environmental-protection.cf", "human-rights-advocacy.tk",
    
    # Subscription traps
    "free-trial-offer.com", "risk-free-trial.net", "cancel-anytime-service.org",
    "no-commitment-required.info", "money-back-guarantee.biz", "satisfaction-guaranteed.co",
    "premium-membership-free.us", "exclusive-access-trial.tk", "vip-service-test.ml",
    "professional-grade-trial.ga", "enterprise-solution-demo.cf", "business-tool-preview.tk",
    
    # Fake software
    "antivirus-free-download.com", "pc-optimizer-tool.net", "registry-cleaner-best.org",
    "driver-updater-automatic.info", "system-speedup-software.biz", "malware-scanner-free.co",
    "password-manager-secure.us", "vpn-service-anonymous.tk", "file-recovery-tool.ml",
    "photo-editor-professional.ga", "video-converter-ultimate.cf", "audio-editor-advanced.tk",
    
    # Educational scams
    "online-degree-accredited.com", "university-diploma-fast.net", "certification-course-free.org",
    "skill-training-guarantee.info", "career-advancement-course.biz", "professional-development.co",
    "language-learning-fast.us", "coding-bootcamp-job.tk", "digital-marketing-master.ml",
    "business-management-mba.ga", "healthcare-certificate.cf", "engineering-degree-online.tk",
    
    # Fake testimonials/reviews
    "customer-reviews-verified.com", "product-testimonials-real.net", "user-feedback-genuine.org",
    "expert-recommendations.info", "doctor-approved-product.biz", "celebrity-endorsed-item.co",
    "scientific-study-proven.us", "laboratory-tested-safe.tk", "clinically-proven-effective.ml",
    "fda-approved-supplement.ga", "patent-pending-formula.cf", "breakthrough-technology.tk",
    
    # Social media impersonation
    "facebook-official.com", "instagram-verified.net", "twitter-authentic.org",
    "linkedin-premium.info", "tiktok-creator.biz", "youtube-partner.co",
    "snapchat-premium.us", "discord-nitro.tk", "telegram-premium.ml",
    "whatsapp-business.ga", "messenger-secure.cf", "viber-official.tk"
]

def get_random_domains(count=30):
    """
    Get a random selection of domains for the game.
    Returns approximately 70% legitimate and 30% suspicious domains.
    """
    legitimate_count = int(count * 0.7)  # 70% legitimate
    suspicious_count = count - legitimate_count  # 30% suspicious
    
    selected_legitimate = random.sample(LEGITIMATE_DOMAINS, min(legitimate_count, len(LEGITIMATE_DOMAINS)))
    selected_suspicious = random.sample(SUSPICIOUS_DOMAINS, min(suspicious_count, len(SUSPICIOUS_DOMAINS)))
    
    # Combine and shuffle
    all_domains = selected_legitimate + selected_suspicious
    random.shuffle(all_domains)
    
    # Create the game data with correct answers
    game_domains = []
    for domain in all_domains:
        is_legitimate = domain in selected_legitimate
        game_domains.append({
            "domain": domain,
            "is_legitimate": is_legitimate
        })
    
    return game_domains

def verify_answers(user_answers, correct_domains):
    """
    Verify user answers against correct classification.
    user_answers: list of {"domain": str, "is_legitimate": bool}
    correct_domains: list of {"domain": str, "is_legitimate": bool}
    
    Returns: {"correct_count": int, "total_count": int, "passed": bool}
    """
    correct_count = 0
    total_count = len(correct_domains)
    
    # Create a lookup dict for correct answers
    correct_lookup = {item["domain"]: item["is_legitimate"] for item in correct_domains}
    
    # Check each user answer
    for user_answer in user_answers:
        domain = user_answer["domain"]
        user_classification = user_answer["is_legitimate"]
        
        if domain in correct_lookup:
            if correct_lookup[domain] == user_classification:
                correct_count += 1
    
    # User passes if they get more than 20 out of 30 correct
    passed = correct_count > 20
    
    return {
        "correct_count": correct_count,
        "total_count": total_count,
        "passed": passed,
        "accuracy": correct_count / total_count if total_count > 0 else 0
    }

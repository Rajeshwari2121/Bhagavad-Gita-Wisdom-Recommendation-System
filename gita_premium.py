import streamlit as st
import pandas as pd
import plotly.express as px
import base64, html
from pathlib import Path
from io import BytesIO
from datetime import date
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
st.set_page_config(page_title="Bhagavad Gita • Wisdom Journey",page_icon="🦚",layout="wide")
VERSES = [{'Problem_Category': 'Stress',
  'Problem': 'Worrying about results',
  'Chapter': 2,
  'Verse': '47',
  'Sanskrit_Shloka': 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।\nमा कर्मफलहेतुर्भूर्मा ते सङ्गोऽस्त्वकर्मणि॥',
  'English_Meaning': 'You have a right to action, not to its fruits. Do not act only for reward, nor '
                     'become attached to inaction.',
  'Telugu_Meaning': 'నీకు కర్మ చేయడంలోనే అధికారం ఉంది; ఫలితాలపై కాదు. ఫలాపేక్షతో పని చేయవద్దు; అకర్మ '
                    'పట్ల కూడా ఆసక్తి చూపవద్దు.',
  'Teaching': 'Focus on sincere effort rather than constant worry about outcomes.',
  'Interpretation': 'The verse encourages responsible action without becoming consumed by results.',
  'Practical_Solution': 'Choose one useful action you can complete today and give it your full '
                        'attention.',
  'Hindi_Meaning': 'तुम्हारा अधिकार कर्म करने में है, उसके फल पर नहीं। फल की आसक्ति और निष्क्रियता '
                   'दोनों से बचो।',
  'Excerpt': False},
 {'Problem_Category': 'Confusion',
  'Problem': 'Feeling unsettled about success and failure',
  'Chapter': 2,
  'Verse': '48',
  'Sanskrit_Shloka': 'योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय।\n'
                     'सिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते॥',
  'English_Meaning': 'Established in yoga, perform your actions without attachment, remaining balanced '
                     'in success and failure; such equanimity is called yoga.',
  'Telugu_Meaning': 'ఓ ధనంజయా! ఆసక్తిని విడిచి, విజయం–అపజయాలలో సమభావంతో కర్మ చేయి. ఈ సమత్వమే యోగం.',
  'Teaching': 'Practice balance in changing circumstances.',
  'Interpretation': 'Steadiness can help when decisions have uncertain outcomes.',
  'Practical_Solution': 'List your options, choose based on values, and accept that outcomes may vary.',
  'Hindi_Meaning': 'आसक्ति छोड़कर सफलता और असफलता में समभाव रखते हुए अपना कर्म करो; यही योग है।',
  'Excerpt': False},
 {'Problem_Category': 'Laziness',
  'Problem': 'Difficulty starting useful work',
  'Chapter': 3,
  'Verse': '8',
  'Sanskrit_Shloka': 'नियतं कुरु कर्म त्वं कर्म ज्यायो ह्यकर्मणः।\n'
                     'शरीरयात्रापि च ते न प्रसिद्ध्येदकर्मणः॥',
  'English_Meaning': 'Perform your prescribed duty, for action is better than inaction; even '
                     'maintaining the body is not possible through inaction.',
  'Telugu_Meaning': 'నీ కర్తవ్యాన్ని నిర్వర్తించు. అకర్మకన్నా కర్మ శ్రేష్ఠమైనది; పనిలేకుండా శరీర పోషణ '
                    'కూడా సాధ్యం కాదు.',
  'Teaching': 'Small consistent action is better than avoidance.',
  'Interpretation': 'Meaningful work and daily responsibility support discipline.',
  'Practical_Solution': 'Start with a ten-minute task, then build momentum.',
  'Hindi_Meaning': 'अपने नियत कर्तव्य का पालन करो; कर्म निष्क्रियता से श्रेष्ठ है।',
  'Excerpt': False},
 {'Problem_Category': 'Confidence',
  'Problem': 'Feeling discouraged and lacking self-belief',
  'Chapter': 6,
  'Verse': '5',
  'Sanskrit_Shloka': 'उद्धरेदात्मनात्मानं नात्मानमवसादयेत्।\nआत्मैव ह्यात्मनो बन्धुरात्मैव रिपुरात्मनः॥',
  'English_Meaning': "One should uplift oneself by oneself, not degrade oneself; the self can be one's "
                     "friend or one's enemy.",
  'Telugu_Meaning': 'మనిషి తనను తానే ఉన్నత స్థితికి తీసుకెళ్లాలి; తనను తాను దిగజార్చుకోకూడదు. మనస్సే '
                    'మిత్రుడు, మనస్సే శత్రువు కావచ్చు.',
  'Teaching': 'Cultivate constructive habits and self-encouragement.',
  'Interpretation': 'Self-discipline and compassionate self-direction can build resilience.',
  'Practical_Solution': 'Write down one strength and one achievable next step.',
  'Hindi_Meaning': 'मनुष्य को स्वयं अपना उत्थान करना चाहिए; मन ही मित्र और शत्रु बन सकता है।',
  'Excerpt': False},
 {'Problem_Category': 'Anger',
  'Problem': 'Anger affecting judgment',
  'Chapter': 2,
  'Verse': '63',
  'Sanskrit_Shloka': 'क्रोधाद्भवति सम्मोहः सम्मोहात्स्मृतिविभ्रमः।\n'
                     'स्मृतिभ्रंशाद् बुद्धिनाशो बुद्धिनाशात्प्रणश्यति॥',
  'English_Meaning': 'From anger arises delusion; from delusion, confusion of memory; from confused '
                     'memory, loss of discernment; and from loss of discernment, ruin.',
  'Telugu_Meaning': 'కోపం వల్ల మోహం, మోహం వల్ల స్మృతిభ్రంశం, దాని వల్ల వివేకనాశనం కలుగుతాయి; వివేకం '
                    'నశిస్తే పతనం సంభవిస్తుంది.',
  'Teaching': 'Anger can interfere with clear judgment.',
  'Interpretation': 'The verse describes how unchecked anger may disrupt thoughtful decisions.',
  'Practical_Solution': 'Before responding, pause, breathe slowly, and revisit the situation calmly.',
  'Hindi_Meaning': 'क्रोध से मोह, स्मृति में भ्रम और विवेक का नाश होता है; इसलिए क्रोध को संभालो।',
  'Excerpt': False},
 {'Problem_Category': 'Fear',
  'Problem': 'Fear of difficult changes',
  'Chapter': 2,
  'Verse': '14',
  'Sanskrit_Shloka': 'मात्रास्पर्शास्तु कौन्तेय शीतोष्णसुखदुःखदाः।\n'
                     'आगमापायिनोऽनित्यास्तांस्तितिक्षस्व भारत॥',
  'English_Meaning': 'Contacts with the senses bring cold and heat, pleasure and pain; they come and go '
                     'and are impermanent. Learn to endure them.',
  'Telugu_Meaning': 'ఇంద్రియస్పర్శల వల్ల చలి–వేడి, సుఖ–దుఃఖాలు కలుగుతాయి. అవి వచ్చి పోతుంటాయి; శాశ్వతం '
                    'కావు. వాటిని సహనంతో ఎదుర్కో.',
  'Teaching': 'Difficult feelings and circumstances can change over time.',
  'Interpretation': 'Patience and perspective can help us face temporary discomfort.',
  'Practical_Solution': 'Identify one safe, manageable step toward the situation you fear.',
  'Hindi_Meaning': 'सुख-दुःख और शीत-उष्ण जैसे अनुभव आते-जाते हैं; धैर्य से उनका सामना करो।',
  'Excerpt': False},
 {'Problem_Category': 'Sadness',
  'Problem': 'Feeling grief or loss',
  'Chapter': 2,
  'Verse': '13',
  'Sanskrit_Shloka': 'देहिनोऽस्मिन्यथा देहे कौमारं यौवनं जरा।\n'
                     'तथा देहान्तरप्राप्तिर्धीरस्तत्र न मुह्यति॥',
  'English_Meaning': 'Just as the embodied self passes through childhood, youth and old age, change is '
                     'part of embodied existence.',
  'Telugu_Meaning': 'దేహంలో బాల్యం, యౌవనం, వృద్ధాప్యం మారుతున్నట్లే జీవితం మార్పులతో సాగుతుంది.',
  'Hindi_Meaning': 'जैसे शरीर में बचपन, युवावस्था और बुढ़ापा आते हैं, वैसे ही जीवन में परिवर्तन आते '
                   'हैं।',
  'Teaching': 'Reflect on change with compassion.',
  'Interpretation': 'The verse addresses the changing condition of embodied life.',
  'Practical_Solution': 'Speak with someone you trust and allow yourself time to grieve.',
  'Excerpt': False},
 {'Problem_Category': 'Jealousy',
  'Problem': 'Comparing yourself with others',
  'Chapter': 12,
  'Verse': '13',
  'Sanskrit_Shloka': 'अद्वेष्टा सर्वभूतानां मैत्रः करुण एव च।\nनिर्ममो निरहङ्कारः समदुःखसुखः क्षमी॥',
  'English_Meaning': 'One who bears no hatred toward beings, and is friendly and compassionate.',
  'Telugu_Meaning': 'అందరిపట్ల ద్వేషం లేకుండా స్నేహం, కరుణ కలిగి ఉండాలి.',
  'Hindi_Meaning': 'सब प्राणियों के प्रति द्वेष रहित, मैत्रीपूर्ण और करुणामय बनो।',
  'Teaching': 'Choose kindness over comparison.',
  'Interpretation': 'Compassion and friendliness oppose envy.',
  'Practical_Solution': 'Celebrate someone else’s success and name one of your own strengths.',
  'Excerpt': False},
 {'Problem_Category': 'Self-doubt',
  'Problem': 'Not trusting your abilities',
  'Chapter': 6,
  'Verse': '6',
  'Sanskrit_Shloka': 'बन्धुरात्मात्मनस्तस्य येनात्मैवात्मना जितः।\n'
                     'अनात्मनस्तु शत्रुत्वे वर्तेतात्मैव शत्रुवत्॥',
  'English_Meaning': 'For one who has mastered oneself, the self is a friend.',
  'Telugu_Meaning': 'తనను తాను నియంత్రించుకున్నవారికి మనస్సు మిత్రుడవుతుంది.',
  'Hindi_Meaning': 'जिसने स्वयं को संयमित किया है, उसके लिए उसका मन मित्र है।',
  'Teaching': 'Build self-trust through disciplined effort.',
  'Interpretation': 'The teaching values inner training and self-mastery.',
  'Practical_Solution': 'Practice one small skill daily and note your progress.',
  'Excerpt': False},
 {'Problem_Category': 'Distraction',
  'Problem': 'Unable to concentrate',
  'Chapter': 6,
  'Verse': '26',
  'Sanskrit_Shloka': 'यतो यतो निश्चरति मनश्चञ्चलमस्थिरम्।\nततस्ततो नियम्यैतदात्मन्येव वशं नयेत्॥',
  'English_Meaning': 'Whenever the restless, unsteady mind wanders, bring it back.',
  'Telugu_Meaning': 'చంచలమైన మనస్సు ఎక్కడికి వెళ్లినా తిరిగి ఏకాగ్రతవైపు తీసుకురావాలి.',
  'Hindi_Meaning': 'चंचल मन जहाँ-जहाँ भटके, उसे फिर से एकाग्रता की ओर लाओ।',
  'Teaching': 'Attention can be trained gently.',
  'Interpretation': 'Mind wandering is expected; returning attention is the practice.',
  'Practical_Solution': 'Work for 15 minutes without notifications, then take a short break.',
  'Excerpt': False},
 {'Problem_Category': 'Overthinking',
  'Problem': 'Thinking constantly about outcomes',
  'Chapter': 2,
  'Verse': '50',
  'Sanskrit_Shloka': 'बुद्धियुक्तो जहातीह उभे सुकृतदुष्कृते।\nतस्माद्योगाय युज्यस्व योगः कर्मसु कौशलम्॥',
  'English_Meaning': 'A person endowed with balanced understanding transcends attachment to good and '
                     'bad results.',
  'Telugu_Meaning': 'సమబుద్ధి కలవారు మంచి చెడు ఫలితాలపై అతిగా ఆసక్తి చూపరు.',
  'Hindi_Meaning': 'समबुद्धि वाला व्यक्ति अच्छे और बुरे परिणामों की आसक्ति से ऊपर उठता है।',
  'Teaching': 'Act wisely without endless mental replay.',
  'Interpretation': 'Equanimity can temper excessive focus on outcomes.',
  'Practical_Solution': 'Set a decision deadline and take the next practical step.',
  'Excerpt': False},
 {'Problem_Category': 'Impatience',
  'Problem': 'Wanting instant results',
  'Chapter': 4,
  'Verse': '38',
  'Sanskrit_Shloka': 'न हि ज्ञानेन सदृशं पवित्रमिह विद्यते।\nतत्स्वयं योगसंसिद्धः कालेनात्मनि विन्दति॥',
  'English_Meaning': 'Nothing in this world is as purifying as knowledge.',
  'Telugu_Meaning': 'ఈ లోకంలో జ్ఞానంతో సమానమైన పవిత్రమైనది మరొకటి లేదు.',
  'Hindi_Meaning': 'इस संसार में ज्ञान के समान पवित्र करने वाला कुछ नहीं है।',
  'Teaching': 'Value learning and gradual growth.',
  'Interpretation': 'Wisdom develops through practice and understanding.',
  'Practical_Solution': 'Choose a realistic weekly learning goal.',
  'Excerpt': False},
 {'Problem_Category': 'Responsibility',
  'Problem': 'Avoiding important duties',
  'Chapter': 3,
  'Verse': '19',
  'Sanskrit_Shloka': 'तस्मादसक्तः सततं कार्यं कर्म समाचर।\nअसक्तो ह्याचरन्कर्म परमाप्नोति पूरुषः॥',
  'English_Meaning': 'Therefore, always perform the work that ought to be done, without attachment.',
  'Telugu_Meaning': 'అందువల్ల ఆసక్తి లేకుండా చేయవలసిన కర్తవ్యాన్ని నిర్వర్తించాలి.',
  'Hindi_Meaning': 'इसलिए आसक्ति रहित होकर अपना आवश्यक कर्तव्य निभाओ।',
  'Teaching': 'Fulfill duties with steadiness.',
  'Interpretation': 'Responsible action matters even without immediate reward.',
  'Practical_Solution': 'Write your three most important responsibilities for today.',
  'Excerpt': False},
 {'Problem_Category': 'Pride',
  'Problem': 'Feeling superior to others',
  'Chapter': 16,
  'Verse': '4',
  'Sanskrit_Shloka': 'दम्भो दर्पोऽभिमानश्च क्रोधः पारुष्यमेव च।\n'
                     'अज्ञानं चाभिजातस्य पार्थ सम्पदमासुरीम्॥',
  'English_Meaning': 'Hypocrisy, arrogance, conceit, anger and harshness are listed as harmful traits.',
  'Telugu_Meaning': 'డాంబికం, గర్వం, అహంకారం, కోపం, కఠినత్వం హానికర లక్షణాలు.',
  'Hindi_Meaning': 'दंभ, घमंड, अभिमान, क्रोध और कठोरता हानिकारक गुण हैं।',
  'Teaching': 'Practice humility and respect.',
  'Interpretation': 'The verse cautions against inflated self-importance.',
  'Practical_Solution': 'Listen to feedback without interrupting.',
  'Excerpt': False},
 {'Problem_Category': 'Forgiveness',
  'Problem': 'Holding resentment',
  'Chapter': 16,
  'Verse': '2',
  'Sanskrit_Shloka': 'अहिंसा सत्यमक्रोधस्त्यागः शान्तिरपैशुनम्।\n'
                     'दया भूतेष्वलोलुप्त्वं मार्दवं ह्रीरचापलम्॥',
  'English_Meaning': 'Nonviolence, truthfulness, freedom from anger, renunciation and peace are '
                     'praised.',
  'Telugu_Meaning': 'అహింస, సత్యం, కోపరాహిత్యం, శాంతి వంటి గుణాలు ప్రశంసించబడ్డాయి.',
  'Hindi_Meaning': 'अहिंसा, सत्य, अक्रोध, त्याग और शांति श्रेष्ठ गुण हैं।',
  'Teaching': 'Release hostility without ignoring boundaries.',
  'Interpretation': 'Forgiveness can coexist with self-protection.',
  'Practical_Solution': 'Write what you can release and what boundary you need.',
  'Excerpt': False},
 {'Problem_Category': 'Loneliness',
  'Problem': 'Feeling disconnected',
  'Chapter': 12,
  'Verse': '14',
  'Sanskrit_Shloka': 'सन्तुष्टः सततं योगी यतात्मा दृढनिश्चयः।\n'
                     'मय्यर्पितमनोबुद्धिर्यो मद्भक्तः स मे प्रियः॥',
  'English_Meaning': 'The devoted practitioner is content, self-controlled and firm in resolve.',
  'Telugu_Meaning': 'సంతృప్తి, ఆత్మనిగ్రహం, దృఢనిశ్చయం కలిగి ఉండాలని బోధిస్తుంది.',
  'Hindi_Meaning': 'संतोष, आत्मसंयम और दृढ़ निश्चय रखने वाले साधक का वर्णन है।',
  'Teaching': 'Cultivate steadiness and meaningful connection.',
  'Interpretation': 'Inner discipline can accompany supportive relationships.',
  'Practical_Solution': 'Reach out to one friend, relative or community group.',
  'Excerpt': False},
 {'Problem_Category': 'Decision-making',
  'Problem': 'Unable to choose a direction',
  'Chapter': 18,
  'Verse': '63',
  'Sanskrit_Shloka': 'इति ते ज्ञानमाख्यातं गुह्याद्गुह्यतरं मया।\nविमृश्यैतदशेषेण यथेच्छसि तथा कुरु॥',
  'English_Meaning': 'Reflect fully on this teaching, then act as you choose.',
  'Telugu_Meaning': 'ఈ బోధనను పూర్తిగా పరిశీలించి, ఆపై నీ నిర్ణయం తీసుకో.',
  'Hindi_Meaning': 'इस उपदेश पर पूरी तरह विचार करो, फिर अपनी इच्छा से निर्णय लो।',
  'Teaching': 'Reflect carefully, then decide.',
  'Interpretation': 'The verse emphasizes deliberation and agency.',
  'Practical_Solution': 'List options, consequences and values before choosing.',
  'Excerpt': False},
 {'Problem_Category': 'Motivation',
  'Problem': 'Losing enthusiasm for work',
  'Chapter': 3,
  'Verse': '21',
  'Sanskrit_Shloka': 'यद्यदाचरति श्रेष्ठस्तत्तदेवेतरो जनः।\nस यत्प्रमाणं कुरुते लोकस्तदनुवर्तते॥',
  'English_Meaning': 'Whatever an exemplary person does, others follow.',
  'Telugu_Meaning': 'ఆదర్శ వ్యక్తి చేసే పనిని ఇతరులు అనుసరిస్తారు.',
  'Hindi_Meaning': 'श्रेष्ठ व्यक्ति जैसा आचरण करता है, दूसरे उसका अनुसरण करते हैं।',
  'Teaching': 'Lead by example through meaningful action.',
  'Interpretation': 'Our conduct can positively influence others.',
  'Practical_Solution': 'Pick one useful action that helps both you and someone else.',
  'Excerpt': False}]
CHAPTERS = [('Arjuna Vishada Yoga',
  'Arjuna’s Despair',
  'अर्जुन का विषाद',
  'అర్జునుని విషాదం',
  'Arjuna faces grief and moral uncertainty before battle.',
  'अर्जुन युद्ध से पहले शोक और नैतिक दुविधा का सामना करता है।',
  'యుద్ధానికి ముందు అర్జునుడు దుఃఖం, ధర్మసంకటాన్ని ఎదుర్కొంటాడు.'),
 ('Sankhya Yoga',
  'Knowledge and Self',
  'ज्ञान और आत्मतत्त्व',
  'జ్ఞానం మరియు ఆత్మతత్త్వం',
  'Krishna teaches the enduring nature of the self, wise action and equanimity.',
  'कृष्ण आत्मा, विवेकपूर्ण कर्म और समत्व का उपदेश देते हैं।',
  'కృష్ణుడు ఆత్మ స్వరూపం, వివేకంతో కర్మ, సమత్వం గురించి బోధిస్తాడు.'),
 ('Karma Yoga',
  'Path of Action',
  'कर्मयोग',
  'కర్మయోగం',
  'Perform your duties sincerely without selfish attachment.',
  'स्वार्थपूर्ण आसक्ति के बिना अपना कर्तव्य निभाओ।',
  'స్వార్థాసక్తి లేకుండా కర్తవ్యాన్ని నిర్వర్తించాలి.'),
 ('Jnana Karma Sannyasa Yoga',
  'Wisdom in Action',
  'ज्ञान और कर्म का समन्वय',
  'జ్ఞానం మరియు కర్మ సమన్వయం',
  'Understand how wisdom transforms the meaning of action.',
  'समझो कि ज्ञान कर्म को कैसे अर्थपूर्ण बनाता है।',
  'జ్ఞానం కర్మకు ఎలా అర్థాన్ని ఇస్తుందో తెలుసుకోండి.'),
 ('Karma Sannyasa Yoga',
  'Renunciation and Action',
  'त्याग और कर्म',
  'త్యాగం మరియు కర్మ',
  'True renunciation concerns attachment, not merely abandoning work.',
  'सच्चा त्याग आसक्ति का त्याग है, केवल काम छोड़ना नहीं।',
  'నిజమైన త్యాగం పనిని వదలడం కాదు; ఆసక్తిని వదలడం.'),
 ('Dhyana Yoga',
  'Meditation and Discipline',
  'ध्यान और अनुशासन',
  'ధ్యానం మరియు క్రమశిక్షణ',
  'A steady mind develops through practice, moderation and meditation.',
  'अभ्यास, संयम और ध्यान से मन स्थिर होता है।',
  'అభ్యాసం, మితాహారం, ధ్యానం వల్ల మనస్సు స్థిరపడుతుంది.'),
 ('Jnana Vijnana Yoga',
  'Knowledge and Realization',
  'ज्ञान और अनुभूति',
  'జ్ఞానం మరియు అనుభూతి',
  'Explore the relationship between divine reality and the world.',
  'ईश्वरतत्त्व और संसार के संबंध को समझो।',
  'దైవతత్త్వం, ప్రపంచం మధ్య సంబంధాన్ని తెలుసుకోండి.'),
 ('Akshara Brahma Yoga',
  'The Imperishable',
  'अक्षर ब्रह्म',
  'అక్షర బ్రహ్మం',
  'Reflect on the imperishable reality and remembrance of the divine.',
  'अविनाशी सत्य और ईश्वर-स्मरण पर चिंतन करो।',
  'నశించని సత్యం, దైవస్మరణపై మననం చేయండి.'),
 ('Raja Vidya Raja Guhya Yoga',
  'Supreme Knowledge',
  'राजविद्या और राजगुह्य',
  'రాజవిద్య రాజగుహ్యం',
  'Devotion and insight reveal the sacred dimension of life.',
  'भक्ति और ज्ञान जीवन के पवित्र पक्ष को प्रकट करते हैं।',
  'భక్తి, జ్ఞానం జీవితంలోని పవిత్రతను తెలియజేస్తాయి.'),
 ('Vibhuti Yoga',
  'Divine Manifestations',
  'ईश्वरीय विभूतियाँ',
  'దైవ విభూతులు',
  'See the divine through excellence, beauty and the wonders of existence.',
  'श्रेष्ठता और सृष्टि के वैभव में दिव्यता का दर्शन करो।',
  'సృష్టి వైభవంలో దైవత్వాన్ని గుర్తించండి.'),
 ('Vishvarupa Darshana Yoga',
  'Universal Form',
  'विश्वरूप दर्शन',
  'విశ్వరూప దర్శనం',
  'Arjuna witnesses the awe-inspiring cosmic form of Krishna.',
  'अर्जुन कृष्ण के विराट विश्वरूप का दर्शन करता है।',
  'అర్జునుడు కృష్ణుని విశ్వరూపాన్ని దర్శిస్తాడు.'),
 ('Bhakti Yoga',
  'Path of Devotion',
  'भक्तियोग',
  'భక్తియోగం',
  'Compassion, humility and steady devotion are central virtues.',
  'करुणा, विनम्रता और स्थिर भक्ति प्रमुख गुण हैं।',
  'కరుణ, వినయం, స్థిరమైన భక్తి ముఖ్య గుణాలు.'),
 ('Kshetra Kshetrajna Vibhaga Yoga',
  'Field and Knower',
  'क्षेत्र और क्षेत्रज्ञ',
  'క్షేత్రం మరియు క్షేత్రజ్ఞుడు',
  'Distinguish the body and experience from the knowing consciousness.',
  'शरीर और अनुभव को जानने वाली चेतना में भेद समझो।',
  'శరీరం, అనుభవం, వాటిని గ్రహించే చైతన్యం మధ్య తేడా తెలుసుకోండి.'),
 ('Gunatraya Vibhaga Yoga',
  'Three Gunas',
  'तीन गुण',
  'మూడు గుణాలు',
  'Sattva, rajas and tamas shape tendencies and behavior.',
  'सत्त्व, रजस् और तमस् प्रवृत्तियों को प्रभावित करते हैं।',
  'సత్త్వ, రజస్, తమస్ గుణాలు ప్రవర్తనను ప్రభావితం చేస్తాయి.'),
 ('Purushottama Yoga',
  'Supreme Person',
  'पुरुषोत्तम योग',
  'పురుషోత్తమ యోగం',
  'Contemplate the changing world and the supreme reality beyond it.',
  'परिवर्तनशील संसार और उससे परे परम सत्य पर चिंतन करो।',
  'మారుతున్న ప్రపంచం, దానికి అతీతమైన పరమ సత్యాన్ని ధ్యానించండి.'),
 ('Daivasura Sampad Vibhaga Yoga',
  'Divine and Harmful Traits',
  'दैवी और आसुरी गुण',
  'దైవీ మరియు ఆసురీ లక్షణాలు',
  'Cultivate honesty, self-control and kindness rather than destructive habits.',
  'सत्य, संयम और दया विकसित करो; हानिकारक आदतों से बचो।',
  'సత్యం, సంయమనం, దయను పెంపొందించి హానికర అలవాట్లను నివారించండి.'),
 ('Shraddhatraya Vibhaga Yoga',
  'Three Forms of Faith',
  'श्रद्धा के तीन प्रकार',
  'మూడు రకాల శ్రద్ధ',
  'Faith, intention and discipline influence our choices.',
  'श्रद्धा, उद्देश्य और अनुशासन हमारे चुनावों को प्रभावित करते हैं।',
  'శ్రద్ధ, ఉద్దేశం, క్రమశిక్షణ మన ఎంపికలను ప్రభావితం చేస్తాయి.'),
 ('Moksha Sannyasa Yoga',
  'Liberation and Surrender',
  'मोक्ष और संन्यास',
  'మోక్షం మరియు సన్యాసం',
  'Krishna concludes with duty, discernment, devotion and surrender.',
  'कृष्ण कर्तव्य, विवेक, भक्ति और समर्पण का सार बताते हैं।',
  'కృష్ణుడు కర్తవ్యం, వివేకం, భక్తి, శరణాగతి సారాన్ని వివరిస్తాడు.')]
IMAGE_B64 = base64.b64encode((Path(__file__).resolve().parent / 'krishna_arjuna.jpg').read_bytes()).decode('ascii')

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');
.stApp{background:radial-gradient(ellipse at 90% 0%,#ffe2d6 0%,transparent 42%),linear-gradient(145deg,#fff9ef,#fff0f3 48%,#f5ecff);color:#34233c;font-family:'Nunito',sans-serif}
[data-testid="stSidebar"]{background:linear-gradient(155deg,#2e164e,#65336d 55%,#9e456c)}
[data-testid="stSidebar"] *{color:#fffaf5!important}
.block-container{max-width:1150px;padding-top:1.25rem}
h1,h2,h3{font-family:'Playfair Display',serif!important;color:#54205e!important}
.hero{background:linear-gradient(115deg,#36164f,#763b83 48%,#cf6d76 85%,#e9a655);border-radius:28px;padding:36px 25px;text-align:center;box-shadow:0 14px 35px #62275935;margin-bottom:22px;border:1px solid #e6b5a0}
.hero h1{color:#fffaf1!important;font-size:clamp(29px,4.1vw,51px);margin:0}
.hero p{color:#fff0d6;font-size:19px;margin:10px 0 0;font-weight:600}
.gcard{background:linear-gradient(125deg,#fffefd,#fff7f0);border:1px solid #e7c5b1;border-radius:22px;padding:22px 25px;margin:14px 0;box-shadow:0 8px 24px #673c5317}
.gcard h3{color:#81396b!important;margin:0 0 12px}.gcard p{line-height:1.85;margin:0;font-size:17px;white-space:pre-wrap}
.verse{font-size:25px;line-height:2.05;text-align:center;white-space:pre-line;color:#652b7c}
[data-testid="stMetric"]{background:linear-gradient(135deg,#fffefd,#ffe9ec);border:1px solid #e4b5c2;border-radius:18px;padding:15px;box-shadow:0 4px 16px #60345815}
div.stButton>button{border-radius:16px;border:1px solid #ce93b1;font-weight:800;min-height:51px;background:#fff9fc;color:#6b2b6c}
div.stButton>button:hover{border-color:#9d4c83;color:#6a2869;background:#fff0f5}
div.stButton>button[kind="primary"]{background:linear-gradient(100deg,#7c3e99,#bd5582,#df8b58);color:white;border:0}
[data-testid="stSelectbox"]>div>div,[data-testid="stTextInput"]>div>div{border-radius:13px}
.peacock{display:inline-block;animation:float 3.6s ease-in-out infinite}@keyframes float{0%,100%{transform:translateY(0) rotate(-7deg)}50%{transform:translateY(-9px) rotate(7deg)}}
.banner-note{text-align:center;color:#87517c;font-weight:700;font-size:16px;margin:8px}
.telugu-verse{font-family:"Noto Sans Telugu","Gautami",sans-serif;color:#a13569;font-size:27px;line-height:2.2}
/* Animated Krishna image: soft floating motion, gold glow and gentle shimmer */
[data-testid="stImage"] img{border-radius:24px;box-shadow:0 12px 35px #8b3d7d50;animation:krishnaFloat 5s ease-in-out infinite,krishnaGlow 6s ease-in-out infinite;max-height:440px;object-fit:contain;background:#fff8eb}
@keyframes krishnaFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
@keyframes krishnaGlow{0%,100%{box-shadow:0 12px 35px #8b3d7d50}50%{box-shadow:0 18px 45px #f2ae4c99}}
@media(prefers-reduced-motion:reduce){[data-testid="stImage"] img,.peacock{animation:none!important}}

/* Additional premium styling */
.stApp{background:radial-gradient(circle at 15% 5%,#ffe4e9 0%,transparent 36%),radial-gradient(circle at 90% 30%,#f5e1ff 0%,transparent 42%),linear-gradient(140deg,#fffaf0,#fdf0f6 55%,#f5edff)!important}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#351046,#692567 58%,#9b496e)!important}
.stButton>button{background:linear-gradient(115deg,#6e248c,#bd5289,#d9a149)!important;color:white!important;border:0!important;border-radius:14px!important;font-weight:750!important;box-shadow:0 5px 15px #6e248c30!important}
.stButton>button:hover{transform:translateY(-2px);filter:brightness(1.07)}

/* Royal purple, antique gold and cream: premium Gita theme */
.stApp{background:radial-gradient(circle at 12% 8%,#fff1d6,transparent 40%),linear-gradient(135deg,#fff9e9,#fff0e9 55%,#f8e8ff)!important}
.hero{background:linear-gradient(115deg,#240d42,#700c4f 65%,#ad4d42)!important;border:2px solid #dba74c!important}
.hero h1{color:#ffe4a4!important}
.gcard{border:1px solid #ecc37b!important;box-shadow:0 8px 22px #6e27501f!important}
.gallery-head{text-align:center;color:#722356;font-family:Georgia,serif;font-size:24px;font-weight:bold;margin:12px 0}
.gallery-frame{border:2px solid #e6b65c;border-radius:16px;padding:7px;background:#fff8e8;box-shadow:0 6px 15px #57244133}
.gallery-label{text-align:center;color:#5e1e52;font-weight:800;font-size:14px;margin:6px 0}
@keyframes gentleGlow{0%,100%{filter:drop-shadow(0 0 4px #ffdf8a)}50%{filter:drop-shadow(0 0 20px #f2b645)}}
.gallery-frame img{animation:gentleGlow 3.8s ease-in-out infinite;object-fit:cover;border-radius:11px}
@media(prefers-reduced-motion:reduce){.gallery-frame img{animation:none}}
</style>""",unsafe_allow_html=True)
df=pd.DataFrame(VERSES)
ASSET_DIR = Path(__file__).resolve().parent
# Only the two original, high-resolution user-provided pictures are retained.
GALLERY = [
    ('Krishna and Arjuna', 'krishna_arjuna.jpg'),
    ('Bhagavad Gita Poster', 'krishna_banner.png'),
]
def artwork_for(problem):
    # Show a clear original image rather than a low-resolution crop.
    if str(problem) in {'Stress', 'Anxiety', 'Distraction', 'Sadness'}:
        return ASSET_DIR / 'krishna_banner.png', 'Bhagavad Gita'
    return ASSET_DIR / 'krishna_arjuna.jpg', 'Krishna guiding Arjuna'

def esc(x):return html.escape(str(x))
def card(t,b):st.markdown(f'<div class="gcard"><h3>{t}</h3><p>{esc(b)}</p></div>',unsafe_allow_html=True)
# Reliable built-in Devanagari -> Telugu-script transliteration.
# This does not translate the meaning; it preserves the Sanskrit sounds.
# No optional package is required.
DEV_CONSONANTS = "क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह ळ क्ष ज्ञ".split()
TEL_CONSONANTS = "క ఖ గ ఘ ఙ చ ఛ జ ఝ ఞ ట ఠ డ ఢ ణ త థ ద ధ న ప ఫ బ భ మ య ర ల వ శ ష స హ ళ క్ష జ్ఞ".split()
DEV_VOWELS = "अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ".split()
TEL_VOWELS = "అ ఆ ఇ ఈ ఉ ఊ ఋ ౠ ఌ ౡ ఏ ఐ ఓ ఔ".split()
DEV_SIGNS = list("ािीुूृॄॢॣेैोौ्")
TEL_SIGNS = list("ాిీుూృౄౢౣేైోౌ్")
SCRIPT_MAP = dict(zip(DEV_CONSONANTS,TEL_CONSONANTS))
SCRIPT_MAP.update(zip(DEV_VOWELS,TEL_VOWELS))
SCRIPT_MAP.update(zip(DEV_SIGNS,TEL_SIGNS))
SCRIPT_MAP.update({'ं':'ం','ः':'ః','ँ':'ఁ','ऽ':'ఽ','ॐ':'ఓం','।':'।','॥':'॥','॑':'॑','॒':'॒'})

def sanskrit_to_telugu(shloka):
    original = str(shloka)
    result = []
    i = 0
    while i < len(original):
        if original[i:i+2] in SCRIPT_MAP:
            result.append(SCRIPT_MAP[original[i:i+2]])
            i += 2
        else:
            result.append(SCRIPT_MAP.get(original[i],original[i]))
            i += 1
    return ''.join(result)

def show_verse(r):
    excerpt='' 
    st.markdown(f'<div class="gcard"><h3>🕉️ Chapter {esc(r["Chapter"])} • Verse {esc(r["Verse"])}{excerpt}</h3><div class="verse">{esc(r["Sanskrit_Shloka"])}</div></div>',unsafe_allow_html=True)
    telugu_script = sanskrit_to_telugu(r['Sanskrit_Shloka'])
    st.markdown(f'<div class="gcard"><h3>🌺 తెలుగు లిపిలో శ్లోకం • Telugu Script</h3><div class="verse telugu-verse">{esc(telugu_script)}</div></div>',unsafe_allow_html=True)
    for title,col in [('📘 English Meaning','English_Meaning'),('🌼 हिंदी अर्थ','Hindi_Meaning'),('🌺 తెలుగు అర్థం','Telugu_Meaning'),('💜 Teaching','Teaching'),('🔮 Interpretation','Interpretation'),('🌱 Practical Solution','Practical_Solution')]:card(title,r[col])
def go(p):st.session_state['nav']=p
pages=['🏠 Home','💜 Find Guidance','📚 18 Chapters','📊 Analytics','🧩 Quiz','🌸 Daily Wisdom']
if 'nav' not in st.session_state:st.session_state.nav=pages[0]
with st.sidebar:
    st.markdown('## 🦚 Krishna Wisdom')
    st.radio('Explore your journey',pages,key='nav')
    st.markdown('---')
    st.caption('18 selectable challenges • 18 complete shlokas • English, Hindi & Telugu • Sanskrit in Telugu script')
st.markdown('<div class="hero"><h1>🕉️ Bhagavad Gita <span class="peacock">🦚</span></h1><p>✨ From Problems to Purpose ✨<br>Wisdom • Courage • Harmony</p></div>',unsafe_allow_html=True)
if st.session_state.nav==pages[0]:
    l,m,r=st.columns([1,3,1])
    with m:
        import streamlit.components.v1 as components
        animated_image = f'''<html><head><style>
          html,body{{margin:0;background:transparent;overflow:hidden}}
          .scene{{height:395px;display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}}
          .halo{{position:absolute;width:85%;height:80%;border-radius:50%;background:radial-gradient(circle,#ffcc72aa 0%,#ed9ec544 45%,transparent 75%);animation:pulse 3s ease-in-out infinite}}
          img{{max-height:345px;max-width:90%;object-fit:contain;border-radius:22px;position:relative;z-index:1;animation:float 4s ease-in-out infinite;box-shadow:0 18px 36px #6c2e6b55}}
          .star{{position:absolute;color:#f5b934;font-size:28px;z-index:2;animation:twinkle 2s ease-in-out infinite alternate}}
          .s1{{top:18%;left:11%}}.s2{{top:29%;right:11%;animation-delay:.6s}}.s3{{bottom:12%;left:18%;animation-delay:1.2s}}
          @keyframes float{{0%,100%{{transform:translateY(4px)}}50%{{transform:translateY(-13px)}}}}
          @keyframes pulse{{0%,100%{{opacity:.5;transform:scale(.92)}}50%{{opacity:1;transform:scale(1.09)}}}}
          @keyframes twinkle{{from{{opacity:.2;transform:scale(.65) rotate(-20deg)}}to{{opacity:1;transform:scale(1.25) rotate(20deg)}}}}
          @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
        </style></head><body><div class="scene"><div class="halo"></div>
        <span class="star s1">✦</span><span class="star s2">✧</span><span class="star s3">✦</span>
        <img alt="Krishna and Arjuna" src="data:image/jpeg;base64,{IMAGE_B64}"></div></body></html>'''
        components.html(animated_image,height=405,scrolling=False)
        st.markdown('<div class="banner-note">🌸 Krishna guiding Arjuna on the path of wisdom 🌸</div>',unsafe_allow_html=True)
        with st.expander('🖼️ View Bhagavad Gita poster', expanded=False):
            st.image(str(ASSET_DIR / 'krishna_banner.png'), use_container_width=True)

    card('✨ Your Personal Wisdom Journey','Choose a life problem, discover a relevant Sanskrit verse, and explore its meaning in English, Hindi and Telugu. Read practical guidance, explore 18 chapters, and test your knowledge.')
    a,b,c=st.columns(3)
    a.metric('Selectable life problems',df.Problem_Category.nunique())
    b.metric('Featured verse selections',len(df))
    c.metric('Chapter summaries',18)
    st.subheader('🌷 Explore Your Journey')
    a,b,c=st.columns(3)
    with a:st.button('💜 Find Guidance',use_container_width=True,type='primary',on_click=go,args=(pages[1],))
    with b:st.button('📚 Explore 18 Chapters',use_container_width=True,on_click=go,args=(pages[2],))
    with c:st.button('📊 Wisdom Analytics',use_container_width=True,on_click=go,args=(pages[3],))
    a,b=st.columns(2)
    with a:st.button('🧩 Take Quiz',use_container_width=True,on_click=go,args=(pages[4],))
    with b:st.button('🌸 Daily Wisdom',use_container_width=True,on_click=go,args=(pages[5],))
elif st.session_state.nav==pages[1]:
    st.header('💜 Select Your Life Problem')
    st.write('**Choose your problem from the list. You do not need to type anything.**')
    categories=sorted(df.Problem_Category.unique().tolist())
    selected=st.selectbox('🌷 What are you facing today?',categories,index=None,placeholder='Select a problem (18 options)...')
    if selected:
        subset=df[df.Problem_Category==selected]
        problems=subset['Problem'].astype(str).tolist()
        st.markdown(f'**Situation:** {esc(problems[0])}')
        if st.button('✨ Show Krishna’s Guidance',type='primary',use_container_width=True):
            st.session_state['guidance_problem']=selected
        if st.session_state.get('guidance_problem')==selected:
            st.success(f'🌼 Guidance for: {selected}')
            art, art_name = artwork_for(selected)
            a_img, a_text = st.columns([1,2])
            with a_img: st.image(str(art),caption=art_name,use_container_width=True)
            with a_text: st.markdown('### 🦚 Krishna’s teaching for your situation')
            
            for _,r in subset.iterrows():show_verse(r)
    else:
        st.info('👆 Select one of the 18 problems to begin your journey.')
    st.caption('This is educational spiritual reflection, not mental-health diagnosis or treatment.')
elif st.session_state.nav==pages[2]:
    st.header('📚 Explore All 18 Chapters')
    ch=st.selectbox('Select chapter',range(1,19),format_func=lambda n:f'Chapter {n} • {CHAPTERS[n-1][0]}')
    name,en,hi,te,s_en,s_hi,s_te=CHAPTERS[ch-1]
    card(f'🌺 Chapter {ch}: {name}',en)
    card('📘 Chapter Summary • English',s_en)
    card('🌼 अध्याय सारांश • हिंदी',s_hi)
    card('🌸 అధ్యాయం సారాంశం • తెలుగు',s_te)
    subset=df[df.Chapter==ch]
    if not subset.empty:
        st.subheader('🕉️ Featured Shlokas')
        idx=st.selectbox('Choose a shloka',list(subset.index),format_func=lambda i:f'Verse {df.loc[i,"Verse"]} • {df.loc[i,"Problem_Category"]}')
        show_verse(df.loc[idx])
    else:st.info('This chapter has a full chapter overview, but no featured Sanskrit verse in the current curated selection.')
elif st.session_state.nav==pages[3]:
    st.header('📊 Wisdom Analytics Dashboard')
    a,b,c=st.columns(3)
    a.metric('Life problems',df.Problem_Category.nunique());b.metric('Featured verses',len(df));c.metric('Chapters represented by verses',df.Chapter.nunique())
    counts=df.Problem_Category.value_counts().rename_axis('Problem').reset_index(name='Count')
    fig=px.bar(counts,x='Problem',y='Count',color='Problem',text='Count',title='Guidance Selections by Problem',color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=False,plot_bgcolor='rgba(0,0,0,0)',paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig,use_container_width=True)
    chapters=pd.DataFrame({'Chapter':list(range(1,19))});chapters['Featured Verses']=chapters.Chapter.map(df.Chapter.value_counts()).fillna(0).astype(int)
    st.plotly_chart(px.bar(chapters,x='Chapter',y='Featured Verses',color='Featured Verses',title='Featured Verses Across 18 Chapters',color_continuous_scale='Sunset'),use_container_width=True)
    a,b=st.columns(2)
    with a:st.plotly_chart(px.pie(counts,names='Problem',values='Count',hole=.5,title='Problem Category Share'),use_container_width=True)
    with b:st.plotly_chart(px.imshow(pd.crosstab(df.Problem_Category,df.Chapter),text_auto=True,aspect='auto',title='Problem–Chapter Connections',color_continuous_scale='Purples'),use_container_width=True)
    st.caption('Charts describe the included curated verses, not the full 700 verses or measured psychological outcomes.')
elif st.session_state.nav==pages[4]:
    st.header('🧩 Bhagavad Gita Knowledge Quiz')
    if 'qidx' not in st.session_state:st.session_state.qidx=0
    if 'score' not in st.session_state:st.session_state.score=0
    if 'answered' not in st.session_state:st.session_state.answered=False
    r=df.iloc[st.session_state.qidx%len(df)]
    st.write(f'Question {st.session_state.qidx+1} • Score {st.session_state.score}')
    card('Which problem best matches this teaching?',r['Teaching'])
    correct=r['Problem_Category'];other=[x for x in sorted(df.Problem_Category.unique()) if x!=correct]
    pool=[correct]+other[:3]
    answer=st.radio('Choose an answer',pool,key=f'answer_{st.session_state.qidx}')
    if st.button('Check Answer',disabled=st.session_state.answered):
        st.session_state.answered=True
        st.session_state['last_answer']=answer
        if answer==correct:st.session_state.score+=1
    if st.session_state.answered:
        if st.session_state['last_answer']==correct:st.success('🌟 Correct!')
        else:st.warning(f'The matching category is: {correct}')
        if st.button('Next Question',type='primary'):
            st.session_state.qidx+=1;st.session_state.answered=False;st.rerun()
elif st.session_state.nav==pages[5]:
    st.header('🌸 Krishna’s Wisdom Explorer')
    st.markdown('**Choose a wisdom topic, discover a new teaching, or explore today’s verse.**')
    WISDOM_TOPICS = [
        ('Peace of Mind','Distraction'),('Selfless Action','Stress'),
        ('Emotional Balance','Confusion'),('Control of Anger','Anger'),
        ('Courage','Fear'),('Self-Discipline','Self-doubt'),
        ('Knowledge','Impatience'),('Devotion','Loneliness'),
        ('Compassion','Jealousy'),('Humility','Pride'),
        ('Freedom from Fear','Fear'),('Patience','Impatience'),
        ('True Friendship','Jealousy'),('Concentration','Distraction'),
        ('Wisdom in Decisions','Decision-making'),
        ('Overcoming Laziness','Laziness'),
        ('Inner Happiness','Sadness'),('Faith and Determination','Motivation')
    ]
    topic_names=[x[0] for x in WISDOM_TOPICS]
    if 'wisdom_topic' not in st.session_state:
        st.session_state.wisdom_topic=topic_names[date.today().toordinal()%len(topic_names)]
    selected_topic=st.selectbox('🪷 Select the wisdom you need',topic_names,
                                index=topic_names.index(st.session_state.wisdom_topic))
    st.session_state.wisdom_topic=selected_topic
    a,b,c=st.columns(3)
    with a:
        if st.button('✨ Give Me New Wisdom',use_container_width=True,type='primary'):
            import random
            alternatives=[x for x in topic_names if x!=st.session_state.wisdom_topic]
            st.session_state.wisdom_topic=random.choice(alternatives)
            st.rerun()
    with b:
        if st.button('🌞 Today’s Wisdom',use_container_width=True):
            st.session_state.wisdom_topic=topic_names[date.today().toordinal()%len(topic_names)]
            st.rerun()
    with c:
        if st.button('🦚 Surprise Me',use_container_width=True):
            import random
            st.session_state.wisdom_topic=random.choice(topic_names)
            st.rerun()
    problem=dict(WISDOM_TOPICS)[st.session_state.wisdom_topic]
    matched=df[df.Problem_Category==problem]
    if not matched.empty:
        r=matched.iloc[0]
        st.markdown(f'<div class="gcard"><h2>🪷 {esc(st.session_state.wisdom_topic)}</h2><p>{esc(r["Teaching"])}</p></div>',unsafe_allow_html=True)
        art, art_name = artwork_for(problem)
        st.image(str(art), caption=art_name, width=340)
        show_verse(r)
        st.info('🌿 Reflection: '+str(r['Practical_Solution']))
    st.caption('The 18 wisdom topics are thematic groupings of the 18 curated verses. Some topics share a verse; they are not 18 additional unique verses.')
st.divider()
st.caption('Bhagavad Gita educational project • 18 complete featured shlokas • Chapter summaries are not the full 700-verse text.')

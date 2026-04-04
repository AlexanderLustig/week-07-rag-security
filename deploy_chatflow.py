import json, urllib.request, ssl, time

FLOWISE_KEY = 'VavTL5SP3yfuHh0b4hW8QQPFKgMEMxnwYBhTFA65Xlo'
OPENAI_CRED = '86627b67-d321-431c-8d64-6c04b58f744f'
CHATFLOW_ID = '2b7b85b7-f7d6-4d2d-99de-97da2b34d9ee'

docs = [
    ('MITRE Initial Access TA0001',
     'MITRE ATT&CK Initial Access Tactic TA0001 covers methods adversaries use to gain a foothold. '
     'Phishing T1566: spearphishing emails with malicious links or attachments targeting specific individuals. '
     'Exploiting Public-Facing Applications T1190: targeting vulnerabilities in web servers, VPN gateways, email servers. '
     'External Remote Services T1133: using VPN, RDP, SSH, Citrix with stolen credentials. '
     'Valid Accounts T1078: using compromised credentials from phishing or data breaches to authenticate normally. '
     'Supply Chain Compromise T1195: compromising software or hardware before delivery to end users. '
     'Drive-by Compromise T1189: watering hole attacks exploiting visitor browsers.'),
    ('MITRE Credential Access TA0006',
     'MITRE ATT&CK Credential Access Tactic TA0006 covers credential theft techniques. '
     'Brute Force T1110: dictionary attacks, password spraying against many accounts, credential stuffing from prior breaches. '
     'OS Credential Dumping T1003: extracting credentials from Windows memory processes, SAM database, Active Directory. '
     'Kerberoasting T1558.003: requesting Kerberos service tickets and cracking them offline. '
     'Input Capture T1056: keyloggers and fake UI overlays to steal credentials. '
     'Steal Web Session Cookie T1539: hijacking authenticated session tokens to bypass MFA. '
     'Unsecured Credentials T1552: finding API keys and passwords in config files, scripts, shell history, cloud metadata.'),
    ('MITRE Lateral Movement TA0008',
     'MITRE ATT&CK Lateral Movement Tactic TA0008 covers techniques to move through networks. '
     'Remote Services T1021: using RDP, SMB file shares, WinRM, SSH to move between systems. '
     'Pass the Hash T1550.002: using NTLM password hashes directly for authentication without cracking. '
     'Pass the Ticket T1550.003: injecting Kerberos authentication tickets into sessions. '
     'Internal Spearphishing T1534: sending phishing from compromised legitimate accounts within the organization. '
     'Taint Shared Content T1080: backdooring files in shared network locations. '
     'Remote Service Session Hijacking T1563: taking over existing authenticated sessions. '
     'Lateral Tool Transfer T1570: moving attack tools between systems via file shares.'),
    ('MITRE Defense Evasion TA0005',
     'MITRE ATT&CK Defense Evasion Tactic TA0005 is the largest tactic covering detection avoidance. '
     'Impair Defenses T1562: disabling antivirus, stopping security services, disabling Windows event logging. '
     'Indicator Removal T1070: clearing event logs, deleting files after use, modifying timestamps. '
     'Obfuscated Files T1027: encoding payloads, packing binaries, command obfuscation with Base64. '
     'Process Injection T1055: injecting code into legitimate running processes like svchost. '
     'Masquerading T1036: naming malware after system processes, placing in expected directories. '
     'Living Off the Land T1218: abusing legitimate system utilities to execute payloads and bypass application controls.'),
    ('NIST Cybersecurity Framework 2.0',
     'NIST Cybersecurity Framework CSF 2.0 released February 2024 adds a sixth function Govern. '
     'GOVERN GV: establishes organizational cybersecurity risk management strategy, expectations, stakeholder roles, supply chain risk management. '
     'IDENTIFY ID: asset management inventories hardware software data, risk assessment identifying threats vulnerabilities likelihood impact. '
     'PROTECT PR: identity management access control MFA privileged access management, data encryption backup, patch management configuration. '
     'DETECT DE: continuous monitoring using SIEM network detection behavioral analytics, mean time to detect exceeds 200 days industry average. '
     'RESPOND RS: incident response procedures preparation detection containment eradication recovery, communication with internal external stakeholders regulators. '
     'RECOVER RC: recovery time objective RTO maximum downtime, recovery point objective RPO maximum data loss, post-incident reviews. '
     'Implementation Tiers range from Tier 1 Partial to Tier 4 Adaptive, most organizations target Tier 3 Repeatable.')
]

def edge(sid, sout, sc, tid, tin, ttype):
    sh = sid + '-output-' + sout + '-' + '|'.join(sc)
    th = tid + '-input-' + tin + '-' + ttype
    return {'source': sid, 'sourceHandle': sh, 'target': tid, 'targetHandle': th,
            'type': 'buttonedge', 'id': sh + '-' + th, 'data': {'label': ''}}

nodes, edges_list = [], []

# 1. ChatOpenAI LLM
nodes.append({'id': 'chatOpenAI_0', 'position': {'x': 1300, 'y': 200}, 'type': 'customNode', 'data': {
    'id': 'chatOpenAI_0', 'label': 'ChatOpenAI', 'version': 6, 'name': 'chatOpenAI',
    'type': 'ChatOpenAI', 'category': 'Chat Models',
    'baseClasses': ['ChatOpenAI', 'BaseChatModel', 'BaseLanguageModel', 'Runnable'],
    'inputAnchors': [], 'inputParams': [],
    'inputs': {'modelName': 'gpt-4o-mini', 'temperature': 0.3},
    'outputAnchors': [{'id': 'chatOpenAI_0-output-chatOpenAI-ChatOpenAI|BaseChatModel|BaseLanguageModel|Runnable',
                       'name': 'chatOpenAI', 'label': 'ChatOpenAI',
                       'type': 'ChatOpenAI | BaseChatModel | BaseLanguageModel | Runnable'}],
    'outputs': {}, 'selected': False, 'credential': OPENAI_CRED
}, 'width': 300, 'height': 380, 'selected': False})

# 2. OpenAI Embeddings
nodes.append({'id': 'openAIEmbeddings_0', 'position': {'x': 50, 'y': 300}, 'type': 'customNode', 'data': {
    'id': 'openAIEmbeddings_0', 'label': 'OpenAI Embedding', 'version': 4, 'name': 'openAIEmbeddings',
    'type': 'OpenAIEmbeddings', 'category': 'Embeddings',
    'baseClasses': ['OpenAIEmbeddings', 'Embeddings'],
    'inputAnchors': [], 'inputParams': [],
    'inputs': {'modelName': 'text-embedding-ada-002', 'stripNewLines': True, 'batchSize': 512},
    'outputAnchors': [{'id': 'openAIEmbeddings_0-output-openAIEmbeddings-OpenAIEmbeddings|Embeddings',
                       'name': 'openAIEmbeddings', 'label': 'OpenAIEmbeddings',
                       'type': 'OpenAIEmbeddings | Embeddings'}],
    'outputs': {}, 'selected': False, 'credential': OPENAI_CRED
}, 'width': 300, 'height': 320, 'selected': False})

# 3. Text Splitter
nodes.append({'id': 'splitter_0', 'position': {'x': 50, 'y': 700}, 'type': 'customNode', 'data': {
    'id': 'splitter_0', 'label': 'Recursive Character Text Splitter', 'version': 2,
    'name': 'recursiveCharacterTextSplitter', 'type': 'RecursiveCharacterTextSplitter',
    'category': 'Text Splitters',
    'baseClasses': ['RecursiveCharacterTextSplitter', 'TextSplitter', 'BaseDocumentTransformer', 'Runnable'],
    'inputAnchors': [], 'inputParams': [],
    'inputs': {'chunkSize': 1000, 'chunkOverlap': 200},
    'outputAnchors': [{'id': 'splitter_0-output-recursiveCharacterTextSplitter-RecursiveCharacterTextSplitter|TextSplitter|BaseDocumentTransformer|Runnable',
                       'name': 'recursiveCharacterTextSplitter', 'label': 'RecursiveCharacterTextSplitter',
                       'type': 'RecursiveCharacterTextSplitter | TextSplitter | BaseDocumentTransformer | Runnable'}],
    'outputs': {}, 'selected': False
}, 'width': 300, 'height': 280, 'selected': False})

# 4. Plain Text document nodes
doc_refs = []  # collect document variable references
for i, (name, text) in enumerate(docs):
    nid = 'plainText_' + str(i)
    doc_refs.append(f'{{{{{nid}.data.instance}}}}')
    nodes.append({'id': nid, 'position': {'x': 500, 'y': 100 + i * 340}, 'type': 'customNode', 'data': {
        'id': nid, 'label': 'Plain Text', 'version': 2, 'name': 'plainText',
        'type': 'Document', 'category': 'Document Loaders', 'baseClasses': ['Document'],
        'inputAnchors': [{'label': 'Text Splitter', 'name': 'textSplitter', 'type': 'TextSplitter',
                          'optional': True, 'id': nid + '-input-textSplitter-TextSplitter'}],
        'inputParams': [],
        'inputs': {
            'text': text,
            'metadata': json.dumps({'source': name}),
            'textSplitter': '{{splitter_0.data.instance}}'  # variable reference
        },
        'outputAnchors': [{'id': nid + '-output-document-Document|json', 'name': 'document',
                           'label': 'Document', 'type': 'Document | json'}],
        'outputs': {'output': 'document'}, 'selected': False
    }, 'width': 300, 'height': 420, 'selected': False})
    edges_list.append(edge('splitter_0', 'recursiveCharacterTextSplitter',
                           ['RecursiveCharacterTextSplitter', 'TextSplitter', 'BaseDocumentTransformer', 'Runnable'],
                           nid, 'textSplitter', 'TextSplitter'))
    edges_list.append(edge(nid, 'document', ['Document', 'json'], 'memoryVectorStore_0', 'document', 'Document'))

# 5. Memory Vector Store — uses variable references for embeddings and documents
nodes.append({'id': 'memoryVectorStore_0', 'position': {'x': 900, 'y': 700}, 'type': 'customNode', 'data': {
    'id': 'memoryVectorStore_0', 'label': 'In-Memory Vector Store', 'version': 1,
    'name': 'memoryVectorStore', 'type': 'Memory', 'category': 'Vector Stores',
    'baseClasses': ['Memory', 'VectorStoreRetriever', 'BaseRetriever'],
    'inputAnchors': [
        {'label': 'Document', 'name': 'document', 'type': 'Document', 'optional': True, 'list': True,
         'id': 'memoryVectorStore_0-input-document-Document'},
        {'label': 'Embeddings', 'name': 'embeddings', 'type': 'Embeddings',
         'id': 'memoryVectorStore_0-input-embeddings-Embeddings'}
    ],
    'inputParams': [{'label': 'Top K', 'name': 'topK', 'type': 'number', 'optional': True, 'default': 4}],
    'inputs': {
        'topK': 4,
        'embeddings': '{{openAIEmbeddings_0.data.instance}}',  # variable reference
        'document': doc_refs  # list of variable references to plainText nodes
    },
    'outputAnchors': [
        {'id': 'memoryVectorStore_0-output-retriever-Memory|VectorStoreRetriever|BaseRetriever',
         'name': 'retriever', 'label': 'Memory Retriever',
         'type': 'Memory | VectorStoreRetriever | BaseRetriever'}
    ],
    'outputs': {'output': 'retriever'}, 'selected': False
}, 'width': 300, 'height': 350, 'selected': False})
edges_list.append(edge('openAIEmbeddings_0', 'openAIEmbeddings',
                       ['OpenAIEmbeddings', 'Embeddings'],
                       'memoryVectorStore_0', 'embeddings', 'Embeddings'))

# 6. Conversational Retrieval QA Chain — variable references for model and retriever
nodes.append({'id': 'chain_0', 'position': {'x': 1300, 'y': 700}, 'type': 'customNode', 'data': {
    'id': 'chain_0', 'label': 'Conversational Retrieval QA Chain', 'version': 3,
    'name': 'conversationalRetrievalQAChain', 'type': 'ConversationalRetrievalQAChain',
    'category': 'Chains',
    'baseClasses': ['ConversationalRetrievalQAChain', 'BaseChain', 'Runnable'],
    'inputAnchors': [
        {'label': 'Chat Model', 'name': 'model', 'type': 'BaseChatModel',
         'id': 'chain_0-input-model-BaseChatModel'},
        {'label': 'Vector Store Retriever', 'name': 'vectorStoreRetriever', 'type': 'BaseRetriever',
         'id': 'chain_0-input-vectorStoreRetriever-BaseRetriever'}
    ],
    'inputParams': [{'label': 'Return Source Documents', 'name': 'returnSourceDocuments',
                     'type': 'boolean', 'optional': True}],
    'inputs': {
        'returnSourceDocuments': True,
        'model': '{{chatOpenAI_0.data.instance}}',                   # variable reference
        'vectorStoreRetriever': '{{memoryVectorStore_0.data.instance}}'  # variable reference
    },
    'outputAnchors': [{'id': 'chain_0-output-conversationalRetrievalQAChain-ConversationalRetrievalQAChain|BaseChain|Runnable',
                       'name': 'conversationalRetrievalQAChain', 'label': 'ConversationalRetrievalQAChain',
                       'type': 'ConversationalRetrievalQAChain | BaseChain | Runnable'}],
    'outputs': {}, 'selected': False
}, 'width': 300, 'height': 380, 'selected': False})
edges_list.append(edge('chatOpenAI_0', 'chatOpenAI',
                       ['ChatOpenAI', 'BaseChatModel', 'BaseLanguageModel', 'Runnable'],
                       'chain_0', 'model', 'BaseChatModel'))
edges_list.append(edge('memoryVectorStore_0', 'retriever',
                       ['Memory', 'VectorStoreRetriever', 'BaseRetriever'],
                       'chain_0', 'vectorStoreRetriever', 'BaseRetriever'))

payload = json.dumps({
    'name': 'Security Knowledge Assistant',
    'flowData': json.dumps({'nodes': nodes, 'edges': edges_list, 'viewport': {'x': 0, 'y': 0, 'zoom': 0.6}}),
    'deployed': True, 'isPublic': True, 'type': 'CHATFLOW'
}).encode()

print(f'Nodes: {len(nodes)}, Edges: {len(edges_list)}, Size: {len(payload)/1024:.1f}KB')

ctx = ssl.create_default_context()
HEADERS = {'Authorization': f'Bearer {FLOWISE_KEY}', 'Content-Type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Deploy
req = urllib.request.Request(
    f'https://cloud.flowiseai.com/api/v1/chatflows/{CHATFLOW_ID}',
    data=payload, method='PUT', headers=HEADERS)
resp = urllib.request.urlopen(req, context=ctx)
print(f'PUT: {resp.status}')

# Wait then test
time.sleep(5)
test_q = json.dumps({'question': 'What are MITRE ATT&CK initial access techniques?'}).encode()
req2 = urllib.request.Request(
    f'https://cloud.flowiseai.com/api/v1/prediction/{CHATFLOW_ID}',
    data=test_q, method='POST', headers=HEADERS)
try:
    resp2 = urllib.request.urlopen(req2, context=ctx, timeout=60)
    result = json.loads(resp2.read())
    if result.get('text'):
        print('SUCCESS! Answer:', result['text'][:500])
    else:
        print('Response:', json.dumps(result)[:300])
except urllib.error.HTTPError as e:
    err_body = e.read()
    try:
        err = json.loads(err_body)
        print('ERROR:', err.get('message', str(err))[:500])
    except:
        print('HTTP ERROR', e.code, err_body[:300])

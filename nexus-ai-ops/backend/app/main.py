import asyncio, random
from datetime import datetime, timezone
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI(title='NEXUS AI Operations Center', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

REQUESTS = Counter('nexus_requests_total', 'Total API requests')
CPU = Gauge('nexus_cpu_percent', 'Simulated CPU usage')
MEM = Gauge('nexus_memory_percent', 'Simulated memory usage')
ERRORS = Counter('nexus_incidents_analyzed_total', 'AI incident analyses')

SERVICES = [
    {'name':'API Gateway','status':'healthy','latency':82},
    {'name':'PostgreSQL','status':'healthy','latency':14},
    {'name':'Redis','status':'healthy','latency':3},
    {'name':'Worker','status':'healthy','latency':41},
    {'name':'AI Analyzer','status':'healthy','latency':126},
]
INCIDENTS = [
    {'id':'INC-1042','severity':'critical','service':'API Gateway','title':'Database connection pool saturation','status':'investigating','time':'2 min ago'},
    {'id':'INC-1041','severity':'warning','service':'Worker','title':'Queue latency increased','status':'resolved','time':'18 min ago'},
]

@app.get('/health')
def health():
    return {'status':'ok','version':'2.0.0','websocket':True}

@app.get('/api/overview')
def overview():
    REQUESTS.inc()
    cpu=random.randint(24,72); mem=random.randint(40,78)
    CPU.set(cpu); MEM.set(mem)
    return {
        'cpu':cpu,'memory':mem,'uptime':'99.98%',
        'services':SERVICES,'incidents':INCIDENTS,
        'requests_per_minute':random.randint(380,920),
        'error_rate':round(random.uniform(.03,.42),2),
        'timestamp':datetime.now(timezone.utc).isoformat()
    }

@app.post('/api/ai/analyze')
def analyze(payload:dict):
    REQUESTS.inc(); ERRORS.inc()
    q=payload.get('question','Analyze the current infrastructure.')
    return {
        'question':q,'confidence':0.91,
        'summary':'The highest-probability fault domain is the database connection layer. API latency increased while database connections approached the configured pool limit.',
        'root_cause':'Connection-pool saturation or a slow query introduced after the latest deployment.',
        'actions':['Inspect active PostgreSQL connections','Check slow-query logs and query duration','Compare metrics before and after the latest deployment','Verify pool size and timeout settings','Roll back only if the regression correlates with the deployment'],
        'signals':['API p95 latency +38%','DB connections 91% of pool','Worker queue +17%','Error rate 0.42%']
    }

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.websocket('/ws/telemetry')
async def telemetry(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            cpu=random.randint(25,70); mem=random.randint(42,76)
            CPU.set(cpu); MEM.set(mem)
            await ws.send_json({
                'type':'telemetry','timestamp':datetime.now(timezone.utc).isoformat(),
                'cpu':cpu,'memory':mem,'requests':random.randint(380,920),
                'latency':random.randint(65,180),'error_rate':round(random.uniform(.02,.45),2),
                'services':[{**s,'latency':max(2,s['latency']+random.randint(-8,12))} for s in SERVICES]
            })
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass

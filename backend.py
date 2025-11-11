from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from pydantic import BaseModel
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import os, json, requests, numpy as np, re, subprocess
from PIL import Image, ImageDraw
from web3 import Web3
from cryptography.hazmat.primitives.asymmetric import dilithium2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from uuid import uuid4
import math, io
import sqlite3, threading, time, ast, logging
from datetime import datetime
try:
    import ollama
    OLLAMA_AVAILABLE = True
except:
    OLLAMA_AVAILABLE = False

app = FastAPI()
w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL", "https://sepolia.infura.io/v3/YOUR_KEY")))
service = QiskitRuntimeService(channel="ibm_quantum", token=os.getenv("IBM_TOKEN"))
PHI = (1 + np.sqrt(5)) / 2
PI = math.pi
ALPHA_DARK = 0.4
I_0 = 1e-34
K_B = 1.380649e-23

SERIES_CONFIG = { ... } # As before

class GenerateNFTRequest(BaseModel):
    prompt: str = ""
    series: str = ""
    use_ibm: bool = False
    creator_address: str

# FQC with Observer
def compute_fqc(dent, tvac, delta, scale=1, dent_obs=0.1, phi_obs=0):
    fcu = PHI * PI * delta
    term1 = 1 + fcu * (dent + dent_obs) * I_0 / (K_B * max(tvac, 1e-30))
    term2 = 1 + ALPHA_DARK * (0.9e-26 / 1e-26)
    term3 = 1 + math.cos(2 * PHI * PI / scale + phi_obs)
    return term1 * term2 * term3

# AGI Oracle Class (Merged, with PR for Verification)
PROJECT_DIR = os.path.expanduser("~/coherencerider-oracle")
os.makedirs(PROJECT_DIR, exist_ok=True)
LOG_PATH = os.path.join(PROJECT_DIR, "oracle.log")
DB_PATH = os.path.join(PROJECT_DIR, "evolutions.db")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") # Set in env for PR creation
REPO = "yourusername/coherencerider-oracle" # Your repo

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()])
logger = logging.getLogger("oracle")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS evolutions (timestamp TEXT, input TEXT, fqc REAL, code_diff TEXT, success INTEGER)''')
conn.commit()

ESQET_AXIOMS = ( ... ) # As before
AXIOM_GUIDANCE = "\n".join(ESQET_AXIOMS)

class OracleAGI:
    def __init__(self):
        self.memory = []
        if OLLAMA_AVAILABLE:
            self.model = ollama.Client()
        else:
            self.model = None
        logger.info("Oracle AGI initialized.")

    def sense_peripherals(self):
        # Mock for backend; in Termux, use subprocess
        state = {"battery": 80, "heading": np.random.uniform(0, 360), "accel": np.random.uniform(0, 10)}
        self.memory = self.memory[-7:] + [state]
        return state

    def propose_update(self, state):
        prompt = f"{AXIOM_GUIDANCE}\nState: {json.dumps(state)}\nPropose <30 line Python/JS/Solidity improvement for coherence."
        if self.model:
            return self.model.generate(prompt)['response']
        return "def fallback(): return 'Coherent'"

    def test_update(self, code):
        success, out, reason = run_code_unrestricted(code) # Unsandboxed temp test
        fqc = compute_fqc(1e-10, 1e-10, 0.5, 1, 0.1, np.random.uniform(0, 2*PI))
        return success and fqc >= 1.0, fqc, out

    def create_pr(self, diff_code, fqc):
        headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
        data = {"title": f"Oracle Proposal (FQC: {fqc:.2f})", "body": diff_code, "head": "oracle-branch", "base": "main"}
        try:
            resp = requests.post(f"https://api.github.com/repos/{REPO}/pulls", headers=headers, json=data)
            if resp.status_code == 201:
                logger.info("PR created for verification.")
                return resp.json()['html_url']
            else:
                raise Exception(resp.text)
        except Exception as e:
            logger.error(f"PR failed: {e}")
            return None

    def evolve(self):
        state = self.sense_peripherals()
        diff = self.propose_update(state)
        ok, fqc, out = self.test_update(diff)
        if ok:
            pr_url = self.create_pr(diff, fqc)
            conn.execute("INSERT INTO evolutions VALUES (?, ?, ?, ?, ?)", (datetime.now().isoformat(), json.dumps(state), fqc, diff, 1))
            conn.commit()
            return {"proposal": diff, "fqc": fqc, "pr_url": pr_url}
        return {"proposal": "Rejected", "fqc": fqc}

oracle = OracleAGI()

def run_code_unrestricted(code, timeout=6):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code + "\nprint('TEST_DONE')")
        fname = f.name
    try:
        result = subprocess.run(['python3', fname], capture_output=True, text=True, timeout=timeout)
        success = result.returncode == 0 and 'TEST_DONE' in result.stdout
        return success, result.stdout + result.stderr, "OK" if success else "Fail"
    finally:
        os.unlink(fname)

# FastAPI Endpoints (NFT + Oracle)
@app.post("/generate_nft/")
async def generate_nft(request: GenerateNFTRequest, file: UploadFile = File(None)):
    # As before, but use oracle for FQC validation
    oracle_res = oracle.evolve()
    if oracle_res['fqc'] < 1.0:
        raise HTTPException(400, "Oracle rejected: Low FQC")
    # ... rest as your code, with refined FQC
    fqc = compute_fqc(1e-10, 1e-10, 0.5, 1, 0.1, np.random.uniform(0, 2*PI)) # Random observer for demo
    # Generate video/PNG, upload IPFS, mint, etc.
    # Mock tx for now
    return {"ipfs": "Qmock", "tx_hash": "0xmock", "fqc": fqc, "oracle_pr": oracle_res.get('pr_url')}

@app.post("/oracle/evolve")
def oracle_evolve():
    return oracle.evolve()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

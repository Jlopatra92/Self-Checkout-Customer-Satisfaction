"""Execute into ignored outputs; leave the public notebook output-free."""
import os
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', '/tmp/self_checkout_matplotlib')
os.environ.setdefault('IPYTHONDIR', '/tmp/self_checkout_ipython')
nb = nbformat.read(ROOT / 'notebooks/01_self_checkout_customer_satisfaction.ipynb', as_version=4)
client = NotebookClient(nb, timeout=300, kernel_name='python3',
                        resources={'metadata': {'path':str(ROOT)}})
client.execute()
out = ROOT / 'outputs/PRIVATE_self_checkout.executed.ipynb'
nbformat.write(nb, out)
print(f'Validated {len(nb.cells)} cells. Private executed notebook: {out}')

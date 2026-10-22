# S2 : Une machine ne suffit plus

> **Salma :** « Le rapport mensuel du trafic fait planter le serveur. Pourquoi ? »

## Avant le TP : installation (en classe)

1. Installer Docker Desktop (ou le charger depuis la clé USB) et le démarrer.
2. Cloner le dépôt, puis vérifier le poste depuis sa racine :

   ```bash
   git clone https://github.com/M2P-git/tp-big-data.git
   cd tp-big-data
   python scripts/verifier_env.py
   ```

3. Charger les images depuis la clé USB (plus rapide que le Wi-Fi) :

   ```bash
   docker load -i E:/images/jupyter-pyspark.tar
   docker load -i E:/images/hadoop-3.5.0.tar
   ```

4. Copier `clickstream_aout.csv` de la clé dans le dossier `data/`.

## Le TP

```bash
docker compose --profile socle up -d
```

Ouvrir <http://localhost:8888>. Un terminal Linux (dans le conteneur) s'ouvre par le menu *File*, *New*, *Terminal*.

### Regarder et mesurer sa machine (avant le notebook)

Dans Windows : le Gestionnaire des tâches (Ctrl + Maj + Échap), onglet Performances, à laisser ouvert.

Dans PowerShell :

```powershell
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores   # processeur
(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB      # mémoire, en Gio
Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size        # SSD ou HDD
ping -n 4 127.0.0.1                                                   # latence locale
ping -n 4 google.com                                                  # latence lointaine
winsat disk -drive c          # débits du disque (PowerShell en administrateur)
docker stats                  # ressources de chaque conteneur, en direct
```

Dans le terminal Jupyter :

```bash
dd if=/dev/zero of=/tmp/essai.bin bs=1M count=1024 conv=fdatasync   # débit d'écriture
dd if=/tmp/essai.bin of=/dev/null bs=1M                            # relecture (cache)
rm /tmp/essai.bin
cat /sys/fs/cgroup/memory.max                                      # mémoire du conteneur
ls -lh ~/work/data/ ; wc -l ~/work/data/clickstream_aout.csv       # le fichier du TP
```

Notez vos mesures : vous les comparerez au débit de pandas mesuré dans le notebook.

### Le notebook

Ouvrir `tp/s2/limite_memoire.ipynb`, et suivre les quatre checkpoints.

Le conteneur Jupyter est volontairement limité à 2 Go de mémoire (voir `compose.yaml`) : c'est notre « petit serveur ».

À la fin de la séance :

```bash
docker compose --profile socle stop
```

## Dossier d'équipe

Premier schéma de la pile cible de votre cas : collecte, stockage, traitement, analyse, restitution.

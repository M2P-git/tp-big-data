# Données des TP

| Fichier | Contenu | Où le trouver |
| --- | --- | --- |
| `echantillon/clickstream_echantillon.csv` | 5 000 événements, pour les tests et les premiers essais | dans le dépôt |
| `echantillon/avis_clients.tsv` | 2 000 avis clients synthétiques (français, darija, mélange) | dans le dépôt |
| `clickstream_aout.csv` | 1,5 Go, environ 11 millions d'événements d'août 2026 | clé USB, ou généré (voir ci-dessous) |

## Le clickstream de Qissaria

Qissaria est une place de marché fictive. Son clickstream suit exactement le format du jeu public **REES46** ([Kaggle, *eCommerce behavior data from multi category store*](https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store)) :

| Colonne | Exemple | Sens |
| --- | --- | --- |
| `event_time` | `2026-08-01 03:56:53 UTC` | horodatage |
| `event_type` | `view`, `cart`, `purchase` | vue, ajout au panier, achat |
| `product_id` | `1779604` | identifiant produit |
| `category_id` | `2053013838392686023` | identifiant de catégorie |
| `category_code` | `electronics.smartphone` | catégorie lisible (parfois vide) |
| `brand` | `atlas` | marque (parfois vide) |
| `price` | `574.79` | prix en dirhams |
| `user_id` | `512066424` | client |
| `user_session` | `0f1a9736-5e49-...` | session de navigation |

Générer le fichier du mois (environ une minute) :

```bash
python scripts/generer_clickstream.py --taille 1.5G --sortie data/clickstream_aout.csv
```

Les options `--lignes`, `--jours`, `--produits`, `--clients` et `--graine` règlent le reste. Avec la même graine, on obtient toujours le même fichier.

Les scripts des TP fonctionnent aussi sur le vrai jeu REES46 (mêmes colonnes) : un mois de ce jeu pèse plusieurs gigaoctets.

## Les avis clients

```bash
python scripts/generer_avis.py --nombre 2000 --sortie data/echantillon/avis_clients.tsv
```

Format : `note<TAB>langue<TAB>texte`. Ces avis sont fabriqués à partir de gabarits, pas collectés.

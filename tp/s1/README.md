# S1 : Pourquoi le Big Data ? (séance sans ordinateur)

> **Salma :** « Le site a enregistré des millions d'événements hier. Suffit-il d'acheter un plus gros serveur ? »

Cette séance se fait sur papier. Deux activités :

## 1. MapReduce sur papier (20 min)

Fiches à imprimer : [`fiches_mapreduce_papier.pdf`](fiches_mapreduce_papier.pdf) (source LaTeX à côté, texte brut dans [`fragments.txt`](fragments.txt)).

Une course : 4 « machines » (un étudiant chacune) contre un « serveur seul ». Chaque machine compte les mots d'un avis client, trie ses mots sur 4 post-it selon la première lettre (A à F, G à M, N à S, T à Z), distribue les post-it, puis additionne ceux qu'elle reçoit. Pendant ce temps, le serveur seul compte les 4 avis à lui tout seul. Une fiche recto-verso par personne. Gardez vos post-it : en S4, vous écrirez le même traitement en Python et vous le lancerez sur un cluster Hadoop.

## 2. La volumétrie de Qissaria (30 min)

La méthode est expliquée en cours, et dans le support (chapitre 1, « Estimer une volumétrie »), sur l'exemple du clickstream : taille d'un événement, volume par jour, durée de conservation, croissance, copies, marge. Elle aboutit à 5,0 To répliqués sur 3 ans, soit 7,2 To de disques.

À vous de l'appliquer aux autres données, en équipes (10 min), avec ces hypothèses (fictives, mais réalistes pour une place de marché régionale) :

| Donnée | Valeur |
| --- | --- |
| Visites par jour | 250 000 |
| Événements par visite | 30 |
| Taille d'un événement | 140 octets |
| Croissance du trafic | +40 % par an |
| Produits au catalogue | 60 000, avec 6 photos de 400 Ko chacun |
| Facteur de réplication | 3 |
| Espace libre à garder | 30 % |

Questions :

1. Les photos : quel volume, avec 3 copies ?
2. Clickstream et photos ensemble, avec 30 % de marge : combien de disques de 4 To ?
3. Qissaria veut aussi garder les journaux de ses serveurs web, dix fois plus volumineux que le clickstream. Quel volume brut (sans les copies) sur 3 ans ? Combien de temps faut-il pour tout relire une fois, à 200 Mo/s ?

Écrivez chaque calcul avec ses unités : c'est ce qui est noté au contrôle.

## Dossier d'équipe

Fiche volumétrie de votre propre cas, avec la même méthode.

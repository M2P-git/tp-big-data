# S1 : Pourquoi le Big Data ? (séance sans ordinateur)

> **Salma :** « Le site a enregistré des millions d'événements hier. Suffit-il d'acheter un plus gros serveur ? »

Cette séance se fait sur papier. Deux activités :

## 1. MapReduce sur papier (20 min)

Fiches à imprimer : [`fiches_mapreduce_papier.pdf`](fiches_mapreduce_papier.pdf) (source LaTeX à côté, texte brut dans [`fragments.txt`](fragments.txt)).

Six groupes comptent les mots de six fragments d'avis clients, échangent des post-it selon la lettre initiale, puis additionnent. Gardez vos post-it : en S4, vous écrirez le même traitement en Python et vous le lancerez sur un cluster Hadoop.

## 2. Estimer la volumétrie de Qissaria (20 min)

Hypothèses (fictives, mais réalistes pour une place de marché régionale) :

| Donnée | Valeur |
| --- | --- |
| Visites par jour | 250 000 |
| Événements par visite | 30 |
| Taille d'un événement | 140 octets |
| Produits au catalogue | 60 000, avec 6 photos de 400 Ko chacun |
| Facteur de réplication | 3 |

Questions :

1. Volume de clickstream par jour, par an ?
2. Volume stocké au bout de 3 ans si le trafic augmente de 40 % par an, réplication comprise ?
3. Volume des photos, réplication comprise ?
4. Combien de disques de 4 To faut-il en tout, si on garde 30 % d'espace libre ?
5. Ces données tiennent-elles sur un seul serveur ? Et si l'on ajoute les journaux techniques des serveurs web, dix fois plus volumineux que le clickstream ?

Écrivez chaque calcul avec ses unités : c'est ce qui est noté au contrôle.

## Dossier d'équipe

Fiche volumétrie de votre propre cas, avec la même méthode.

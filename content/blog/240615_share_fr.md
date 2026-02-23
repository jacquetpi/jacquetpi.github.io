---
title: "On the importance of sharing Cloud resources"
date: 2024-06-15
summary: "[French] Sharing Cloud resources is a way to reduce the environmental impact of ICT"
---

Le *Cloud Computing* est un produit très prisé des entreprises.
Il permet de déléguer à un tiers la gestion de ses serveurs informatiques afin de se concentrer sur le développement de ses logiciels.
Ces tiers, ce sont les fournisseurs Cloud.
Certains ont des activités annexes les rendant connus du grand public (*Google Cloud Platform*, *Amazon Web Services*), d'autres moins (*OVHcloud*), mais ils ont tous un point commun : **la gestion de grands centres de données** (les *data centers*) qui hébergent un très grand nombre de serveurs de calcul.

Depuis quelques années, l'empreinte environnementale des *data centers* est scrutée de près. Elle pourrait compter jusqu'à [42% du total](https://hubblo.org/fr/blog/datacenters-imported-impacts/) de l'empreinte carbone du numérique, elle-même estimée entre [2,1% et 3,9%](https://www.sciencedirect.com/science/article/pii/S2666389921001884?via%3Dihub) des émissions de gaz à effet de serre mondial. Ces chiffres sur les émissions carbone feraient presque oublier [les autres impacts](https://www.lemonde.fr/sciences/article/2023/05/01/la-recherche-au-defi-de-la-sobriete-energetique-du-numerique_6171677_1650684.html) du Cloud :

- l'épuisement des ressources naturelles,
- l'acidification de l'air,
- etc.

Plus que les valeurs elle-même, c'est surtout la forte croissance de celles-ci qui inquiète, avec un potentiel **doublement des émissions carbones d'ici à [2030](https://www.arcep.fr/la-regulation/grands-dossiers-thematiques-transverses/lempreinte-environnementale-du-numerique/etude-ademe-arcep-empreinte-environnemental-numerique-2020-2030-2050.html)**.

L'efficacité énergétique des *data centers* n'a pourtant, et paradoxalement, **jamais été [aussi bonne](https://joint-research-centre.ec.europa.eu/jrc-news-and-updates/eu-code-conduct-data-centres-towards-more-innovative-sustainable-and-secure-data-centre-facilities-2023-09-05_en)**. Car c'est bien l'[augmentation des usages](https://www.iea.org/energy-system/buildings/data-centres-and-data-transmission-networks#programmes) qui est la principale cause de cette augmentation de la demande énergétique. À l'heure où les acteurs cherchent à réduire leur impact environnemental, il reste pourtant un tabou : celui du **partage des ressources de calcul** entre les usagers.

## Le Cloud, un modèle de covoiturage ?

Le *Cloud computing* repose sur un modèle de **virtualisation** des ressources matérielles. Un serveur physique est "découpé" en plus petites unités virtuelles pour le partager entre plusieurs clients. Ses composants électroniques sont **mutualisés** : plusieurs serveurs virtuels se partagent une seule carte mère, une seule carte réseau. On retrouve la même logique dans le covoiturage : il vaut mieux remplir un véhicule plutôt que chacun utilise le sien.

Mais, ce modèle de covoiturage dans le Cloud n'est pas pleinement exploité, car **il ne se décline pas sur le principal composant utile des serveurs : ceux associés au calcul**. Un serveur possède des dizaines d'unités de calcul (cœurs de CPU), répartis entre les clients en fonction de leurs besoins. Louer des unités entières est cependant loin d'être optimal, car tous les clients n'ont pas besoin en permanence de toutes leurs capacités de calculs.

Alors pourquoi ne pas les partager dans ce cas ?

## La sur-allocation, un modèle de partage

Partager une unité de calcul revient à **placer plusieurs clients dessus**. On loue alors plus de ressources virtuelles que physiquement disponibles. Certains auront peut-être reconnu le mécanisme de sur-réservation des compagnies aériennes (aussi connu sous sa version anglaise, le surbooking). En partant du principe que tous les voyageurs ne se présenteront pas à l'embarquement, il est envisageable de vendre plus de billets qu'il n'y a de places pour s'assurer un taux de remplissage optimal de l'avion.

À cause de cette origine, et des désagréments qu'elle peut causer si des clients ne peuvent embarquer, la technique pâtit d'une mauvaise presse auprès de ses clients. Bien qu'il soit légitime de se sentir lésé face à un refus d'embarquement, le contexte du Cloud est néanmoins différent : les ressources virtuelles peuvent être rapidement déplacées depuis un serveur surchargé vers le reste de l'infrastructure. On peut en revanche identifier deux **freins majoritaires**, venant de la sécurité et des performances.

Le partage des ressources de calcul pose la problématique de la **confidentialité des calculs**. Deux clients placés sur un même cœur peuvent potentiellement mesurer des activités du CPU afin d'essayer de déduire des secrets cryptographiques appartenant au second. Ces méthodes, connues sous le nom d'attaques par canaux auxiliaires, sont cependant particulièrement complexes à mettre en place.

Dès lors, la **performance**—c'est-à-dire la vitesse à laquelle les calculs sont réalisés—reste le principal frein au partage des ressources. En effet, la vitesse de traitement peut être affectée par un système sur-réservé (en informatique, on parle de sur-allocation, d'overcommitment ou d'oversubscription) car une unité de calcul doit alors partager son temps disponible entre ses clients attribués. Cependant, ce ralentissement peut être contenu par les fournisseurs Cloud :

- En étudiant minutieusement quelles ressources sont activement utilisées
- Et, en prédisant dans quel mesure elles continueront à l'être, avant de déployer de nouveaux clients sur un serveur.

Ce domaine, appelé **"sur-allocation dynamique"**, est activement étudié par la communauté de recherche académique et industrielle [[cf](https://dl.acm.org/doi/abs/10.1145/3132747.3132772), [cf](https://dl.acm.org/doi/abs/10.1145/3447786.3456259)].

## Qui utilise la sur-allocation?

On peut tracer les origines de la sur-allocation dès 1970. Les ordinateurs, alors très coûteux, n'avaient d'autres choix que de partager leur unique unité de calcul entre [les premiers systèmes virtuels](https://ieeexplore.ieee.org/abstract/document/5388296).

L'apparition d'architectures à plusieurs cœurs, jointe à la baisse des coûts, a ensuite permis d'éviter de sur-allouer les environnements Cloud de production. Il se trouve que la sur-allocation n'est aujourd'hui associée qu'à [certaines offres](https://docs.aws.amazon.com/whitepapers/latest/security-design-of-aws-nitro-system/the-ec2-approach-to-preventing-side-channels.html) et [certaines gammes tarifaires](https://www.ovhcloud.com/en/public-cloud/sandbox/).

La performance demeure un [argument marketing](https://www.stackscale.com/blog/oversubscription-cloud-computing/#Who_does_usually_oversubscribe_resources) semblant fonctionner. Le milieu informatique, bercé par la [loi de Moore](https://fr.wikipedia.org/wiki/Loi_de_Moore), n'est probablement pas habitué à réduire ses performances matérielles. Pourtant, tous les cas d'usage ne nécessitent pas un niveau de performance optimal. Estimer les besoins réels des clients, allant de l'hébergement du site d'une boulangerie jusqu'aux applications "temps réel" est donc primordial.

## Les gains potentiels

Partager les ressources de calcul apparaît comme incontournable pour contenir la progression des usages. En effet, **le calcul est [le facteur limitant](https://www.usenix.org/conference/osdi20/presentation/ambati) dans la plupart des contextes Cloud**. Autrement dit, les premières ressources manquantes sur les serveurs, celles qui conduisent les fournisseurs Cloud à installer de nouveaux équipements physiques, sont les cœurs de calcul. Les partager, c'est potentiellement réduire la taille des *data centers* de manière significative.

La consommation énergétique des *data centers* pourrait alors s'en trouver drastiquement réduite. Un serveur a une consommation relativement [logarithmique](https://www.sciencedirect.com/science/article/pii/S0167739X17304910). Sa consommation au repos est significative, alors qu'une variation de charge entre 40% et 80% n'a, en comparaison, qu'un faible impact. **Il est préférable de charger davantage certains serveurs, afin d'en éteindre d'autres**. Ainsi, on peut réaliser d'importantes économies d'énergie tout en réduisant l'impact environnemental grâce à un rationnement du nombre de serveurs nécessaires.

L'intérêt environnemental semble donc démontré, mais les considérations de performance continuent de l'emporter. Néanmoins, doit-on encore privilégier la performance à tout prix face aux enjeux climatiques ? Cela semble être la prochaine question à laquelle se confrontera le numérique dans les années à venir, tandis que la société est peu à peu amenée à s'interroger sur une autre question, potentiellement plus épineuse : nos usages numériques pourront-ils continuellement augmenter ?

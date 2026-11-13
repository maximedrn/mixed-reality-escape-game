// Tohannic : No Way Out
// Inventaire détaillé des ressources à créer, adapter ou intégrer
// Projet INF3001 / INF3002 — Meta Quest 3
// Compiler avec Typst : typst compile inventaire_assets_tohannic.typ

#set document(
  title: "Tohannic : No Way Out — Inventaire détaillé des assets",
  author: "Équipe du projet"
)
#set page(
  paper: "a4",
  margin: (top: 1.7cm, bottom: 1.7cm, left: 1.8cm, right: 1.8cm),
  numbering: "1"
)
#set text(font: "New Computer Modern", size: 9.5pt)
#set par(justify: true, leading: 0.62em)
#set heading(numbering: "1.1")
#set table(
  inset: 5pt,
  stroke: 0.45pt + luma(190),
  align: left
)

#let accent = rgb("#71343B")
#let dark = rgb("#30343B")
#let pale = rgb("#F4ECEC")
#let pale-blue = rgb("#EAF0F5")
#let pale-gold = rgb("#F7F0E2")
#let tag(label, color) = box(
  fill: color,
  radius: 3pt,
  inset: (x: 5pt, y: 2pt)
)[#text(size: 8pt, weight: "bold")[#label]]
#let priority(p) = if p == "Indispensable" {
  tag("INDISPENSABLE", rgb("#F7E3E4"))
} else if p == "Important" {
  tag("IMPORTANT", rgb("#E7EEF5"))
} else {
  tag("OPTIONNEL", rgb("#F6EEDC"))
}
#let status(s) = text(size: 8pt, fill: luma(85))[#s]

#align(center)[
  #v(10pt)
  #text(size: 11pt, weight: "bold", fill: accent)[DOSSIER DE PRODUCTION]
  #v(5pt)
  #text(size: 25pt, weight: "bold", fill: dark)[TOHANNIC : NO WAY OUT]
  #v(4pt)
  #text(size: 15pt, weight: "semibold")[Inventaire détaillé des assets]
  #v(8pt)
  #text(size: 10pt, fill: luma(90))[Escape game en réalité mixte — Meta Quest 3]
  #v(12pt)
  #line(length: 75%, stroke: 1.4pt + accent)
  #v(9pt)
  #text(size: 9pt)[INF3001 — Simulation et Applications Interactives]
  #text(size: 9pt)[INF3002 — Mouvements et Intelligence Artificielle]
  #v(5pt)
  #text(size: 9pt, fill: luma(100))[Document de référence pour la préparation, la modélisation et l'intégration]
  #v(12pt)
]

#block(fill: pale, radius: 5pt, inset: 10pt)[
  *Objectif du document*

  Recenser les ressources nécessaires au prototype *Tohannic : No Way Out*,
  préciser leur contenu, leur rôle dans le jeu, leur priorité et l'outil
  recommandé. L'inventaire distingue les ressources réellement à modéliser
  dans Blender, les éléments à construire directement dans Unity, les éléments
  fournis par l'environnement réel via Meta Scene API / MRUK et les ressources
  à récupérer ou produire séparément (sons, marqueurs, animations).
]

#v(8pt)
#text(size: 9pt, fill: luma(90))[Version de travail — basée sur la proposition de projet fournie par l'équipe.]

= Comment lire cet inventaire

- *Indispensable* : nécessaire à la boucle de jeu minimale ou à une exigence explicitement annoncée dans le projet.
- *Important* : améliore la lisibilité, la qualité ou la robustesse, sans être toujours bloquant pour le premier prototype.
- *Optionnel* : extension à envisager uniquement après validation du parcours principal.
- *À récupérer / adapter* : une ressource existante peut être utilisée après vérification de sa licence, de son format et de sa compatibilité.
- *À créer* : ressource à fabriquer ou à assembler pour répondre au besoin du projet.

Les priorités portent sur le prototype décrit dans le cahier des charges. Elles ne signifient pas que chaque élément doit obligatoirement être un modèle Blender : plusieurs éléments peuvent être des primitives, des composants Unity ou des données de scène.

= 1. Périmètre du prototype

Le prototype initial se déroule dans *une seule pièce réelle*. Le joueur voit cette pièce en passthrough sur le Meta Quest 3. Il doit trouver et manipuler trois indices virtuels, résoudre les énigmes, saisir un code sur un clavier virtuel et atteindre une sortie virtuelle. Un monstre virtuel se déplace dans la pièce, détecte le joueur selon son champ de vision et les obstacles, le poursuit puis recherche sa dernière position connue.

Le projet repose sur deux ensembles complémentaires :

- *MVP 1 — INF3001* : environnement de réalité mixte, calibration, mobilier suivi, interactions avec les trois indices et progression jusqu'à la sortie.
- *MVP 2 — INF3002* : personnage animé à partir de captures FreeMoCap, navigation avec NavMesh et comportement piloté par une machine à états finis (FSM).

*Conséquence pour la production 3D :* la priorité n'est pas de reconstruire artistiquement toute la pièce. La géométrie de la pièce doit d'abord provenir de la Scene API / MRUK. Les modèles Blender servent surtout au monstre et aux objets virtuels manipulables.

= 2. Vue d'ensemble des ressources

#table(
  columns: (0.55fr, 2.1fr, 1.25fr, 1.15fr, 1fr),
  [*N°*], [*Famille*], [*Outil principal*], [*MVP*], [*Priorité*],
  [01], [Monstre : modèle, rig et matériaux], [Blender], [MVP 2], [Indispensable],
  [02], [Animations du monstre], [FreeMoCap, Blender, Unity], [MVP 2], [Indispensable],
  [03], [Plaque et symbole], [Blender / Unity], [MVP 1], [Indispensable],
  [04], [Disque gradué et support], [Blender / Unity], [MVP 1], [Indispensable],
  [05], [Fragments et objet assemblé], [Blender / Unity], [MVP 1], [Indispensable],
  [06], [Clavier et sortie virtuelle], [Unity / Blender], [MVP 1], [Indispensable],
  [07], [Architecture et mobilier représentés], [MRUK / Unity], [MVP 1 et 2], [Indispensable],
  [08], [Marqueurs QR des meubles suivis], [Génération graphique], [MVP 1], [Indispensable],
  [09], [Interface, retours et effets], [Unity], [MVP 1 et 2], [Important],
  [10], [Sons et ambiance], [Banque audio / création], [MVP 1 et 2], [Important],
  [11], [Objets supplémentaires et extensions], [Blender / Unity], [Après MVP 2], [Optionnel]
)

= 3. Personnage principal : le monstre

#priority("Indispensable")
Le monstre est un personnage 3D déformable. Il doit être associé à un squelette,
à des poids de skinning et à des animations utilisables dans Unity. L'équipe a
déjà téléchargé un modèle de Goblin comprenant notamment des fichiers
`.blend`, `.blend1`, `.fbx` et une texture de palette. Il faut d'abord *auditer
et adapter ce modèle existant* avant d'envisager une nouvelle modélisation.

== 3.1 Modèle et géométrie

#table(
  columns: (1.45fr, 3.15fr, 1.05fr, 0.9fr),
  [*Élément*], [*Contenu attendu / vérification*], [*Outil*], [*Priorité*],
  [Corps complet], [Silhouette cohérente et lisible à distance ; proportions adaptées à la pièce et au casque.], [Blender], [Indispensable],
  [Tête], [Volume du crâne, visage, mâchoire et zones expressives.], [Blender], [Indispensable],
  [Yeux], [Géométrie ou surfaces des yeux ; matériau suffisamment contrasté pour rendre le regard visible.], [Blender], [Important],
  [Bouche et dents], [Mâchoire et dents si elles sont présentes dans le modèle ; vérifier qu'elles ne traversent pas le visage pendant l'animation.], [Blender], [Important],
  [Torse et bassin], [Volumes du torse, de l'abdomen et du bassin raccordés au squelette.], [Blender], [Indispensable],
  [Bras et avant-bras], [Deux membres, avec une topologie qui supporte la flexion des coudes.], [Blender], [Indispensable],
  [Mains et doigts], [Mains suffisamment lisibles ; doigts séparés si le modèle le permet. Griffes uniquement si elles font partie du design retenu.], [Blender], [Important],
  [Cuisses et jambes], [Deux membres inférieurs avec une topologie adaptée aux genoux.], [Blender], [Indispensable],
  [Pieds], [Pieds orientés correctement et adaptés aux poses de marche et de course.], [Blender], [Indispensable],
  [Détails de silhouette], [Cornes, oreilles, excroissances, vêtements ou accessoires uniquement s'ils existent dans le modèle choisi.], [Blender], [Optionnel]
)

== 3.2 Préparation du rig et du skinning

#table(
  columns: (1.45fr, 3.15fr, 1.05fr, 0.9fr),
  [*Élément*], [*Travail à effectuer*], [*Outil*], [*Priorité*],
  [Armature], [Vérifier la hiérarchie des os, les noms, les orientations et les relations parent-enfant.], [Blender], [Indispensable],
  [Os du bassin et du tronc], [Contrôler bassin, colonne, poitrine et cou selon la structure du personnage.], [Blender], [Indispensable],
  [Os des bras], [Contrôler épaules, bras, avant-bras et mains des deux côtés.], [Blender], [Indispensable],
  [Os des jambes], [Contrôler cuisses, genoux, chevilles et pieds des deux côtés.], [Blender], [Indispensable],
  [Weight painting], [Attribuer et corriger les influences des os sur les sommets ; éviter les déformations excessives.], [Blender], [Indispensable],
  [Tests articulaires], [Tester épaules, coudes, poignets, hanches et genoux avec des poses extrêmes raisonnables.], [Blender], [Indispensable],
  [Échelle et orientation], [Vérifier l'échelle, l'axe vertical, l'origine et les transformations avant export.], [Blender], [Indispensable],
  [Blend shapes], [Préparer des formes correctives ou expressives pour le visage ou les membres, si l'extension est retenue.], [Blender], [Optionnel]
)

== 3.3 Matériaux et textures du monstre

#table(
  columns: (1.45fr, 3.15fr, 1.05fr, 0.9fr),
  [*Élément*], [*Contenu attendu / vérification*], [*Outil*], [*Priorité*],
  [Matériau de peau], [Couleur et finition cohérentes ; éviter les matériaux trop complexes pour le casque autonome.], [Blender / Unity], [Indispensable],
  [Texture ou palette], [Vérifier que la texture fournie avec le Goblin est bien reliée au matériau et exportée.], [Blender], [Indispensable],
  [Matériau des yeux], [Contraste suffisant pour identifier l'orientation du visage.], [Blender / Unity], [Important],
  [Matériau des dents], [À conserver seulement si le modèle comporte des dents visibles.], [Blender / Unity], [Optionnel],
  [Matériaux secondaires], [Cornes, griffes, vêtements ou accessoires présents dans le modèle.], [Blender / Unity], [Optionnel]
)

== 3.4 Contrôles avant intégration

- Le personnage s'importe dans Unity sans pièce manquante.
- Le maillage est relié à la bonne armature.
- Les matériaux et textures sont correctement affectés.
- Les articulations ne présentent pas de déformations bloquantes.
- Le personnage tient dans l'espace de jeu et ne dépasse pas les limites de sécurité.
- Le modèle et ses animations restent suffisamment légers pour le Quest 3.

= 4. Animations du monstre : motion capture

#priority("Indispensable")
Les animations sont des ressources distinctes du modèle 3D. Elles sont
enregistrées avec FreeMoCap, nettoyées dans Blender, transférées au squelette
du monstre (retargeting), puis intégrées dans Unity.

== 4.1 Clips minimaux

#table(
  columns: (1.2fr, 2.8fr, 1.25fr, 0.9fr),
  [*Clip*], [*Action et usage dans le jeu*], [*Source / outil*], [*Priorité*],
  [Idle], [Pose de repos ; utile pour éviter un personnage immobile dans une pose de marche. À capturer ou créer selon le temps disponible.], [FreeMoCap / Blender], [Important],
  [Walk], [Marche utilisée pendant la patrouille et les déplacements lents.], [FreeMoCap], [Indispensable],
  [Run], [Course utilisée pendant la poursuite ; vitesse et amplitude adaptées au personnage.], [FreeMoCap], [Indispensable],
  [Search], [Mouvement de recherche sur place : regarder autour de soi ou pivoter.], [FreeMoCap], [Important],
  [Attack / Capture], [Mouvement bref associé à la capture ; à ajouter si la qualité est suffisante.], [FreeMoCap], [Important],
  [Detection], [Réaction visuelle à la détection du joueur ; peut être une animation courte ou une transition d'état.], [FreeMoCap / Unity], [Optionnel]
)

Le cahier des charges impose au minimum deux animations issues de FreeMoCap :
la marche et la course. Les autres clips ne doivent pas retarder cette exigence.

== 4.2 Ressources techniques d'animation

- Séquences vidéo ou enregistrements nécessaires à la reconstruction du mouvement.
- Calibration préalable des caméras utilisées par FreeMoCap.
- Données de mouvement reconstruites par FreeMoCap.
- Fichiers de mouvement nettoyés et corrigés dans Blender.
- Squelette de référence du monstre.
- Animations retargetées sur ce squelette.
- Clips exportés et importés dans Unity.
- Contrôleur Animator et transitions entre les états.

== 4.3 États de l'IA et animations associées

#table(
  columns: (1.25fr, 1.35fr, 2.6fr),
  [*État FSM*], [*Animation indicative*], [*Comportement attendu*],
  [Patrouille], [Walk], [Le monstre suit des points de passage prédéfinis.],
  [Détection], [Detection ou réaction], [Le joueur entre dans le champ de vision et la ligne de vue est libre.],
  [Poursuite], [Run], [Le monstre rejoint la position actuelle du joueur tant qu'il le voit.],
  [Perte de cible], [Transition vers Search], [Le monstre cesse de recevoir la position actuelle du joueur.],
  [Recherche], [Search], [Le monstre rejoint la dernière position observée et inspecte brièvement la zone.],
  [Retour en patrouille], [Walk], [Le monstre reprend son parcours après la recherche.],
  [Capture], [Attack ou animation dédiée], [La proximité déclenche la défaite sans contact physique réel.]
)

= 5. Objets des trois énigmes

#priority("Indispensable")
Les trois indices sont des objets virtuels 3D ancrés dans la pièce. Ils sont
saisis, déplacés, tournés ou assemblés avec le suivi des mains. Pour chaque
objet, prévoir un maillage visible, un collider simplifié, un pivot cohérent et
une zone de préhension adaptée.

== 5.1 Indice 1 — Plaque à examiner

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Asset*], [*Spécification détaillée*], [*Outil*], [*Priorité*],
  [Plaque principale], [Plaque rectangulaire ou de forme choisie par l'équipe ; épaisseur visible et dimensions adaptées à la prise en main.], [Blender], [Indispensable],
  [Face révélant le symbole], [Face portant le symbole à découvrir en orientant la plaque.], [Blender], [Indispensable],
  [Symbole gravé], [Forme géométrique identifiable ; relief ou gravure selon le style retenu.], [Blender / texture], [Indispensable],
  [Face secondaire], [Face opposée ou côtés ; peuvent rester simples si aucun indice n'y figure.], [Blender], [Important],
  [Matériau de plaque], [Métal, pierre ou autre finition ; choisir un matériau lisible en passthrough.], [Blender / Unity], [Important],
  [Collider], [Volume de collision simple correspondant à la plaque.], [Unity], [Indispensable],
  [Pivot et prise en main], [Origine placée de façon à permettre une rotation intuitive dans la main.], [Blender / Unity], [Indispensable]
)

*Comportements associés à programmer dans Unity :* sélection par la main,
prise, rotation, relâchement et validation de l'orientation permettant de
révéler le symbole. Ces comportements ne sont pas des modèles 3D.

== 5.2 Indice 2 — Disque gradué

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Asset*], [*Spécification détaillée*], [*Outil*], [*Priorité*],
  [Disque principal], [Disque circulaire avec épaisseur suffisante pour être visible et manipulable.], [Blender], [Indispensable],
  [Graduations], [Repères réguliers sur le pourtour ; géométrie ou texture selon le niveau de détail.], [Blender / texture], [Indispensable],
  [Symboles], [Un ou plusieurs symboles permettant l'alignement avec l'indice précédent.], [Blender / texture], [Indispensable],
  [Repère fixe], [Marqueur visuel qui sert de référence pendant la rotation.], [Blender / Unity], [Indispensable],
  [Support], [Base fixe maintenant le disque dans une position cohérente, si le scénario le nécessite.], [Blender], [Important],
  [Collider], [Collider simple pour le disque et, si nécessaire, collider séparé pour le support.], [Unity], [Indispensable],
  [Pivot de rotation], [Axe central configuré pour une rotation contrôlée.], [Blender / Unity], [Indispensable]
)

*Comportements associés à programmer dans Unity :* prise en main,
rotation autour de l'axe prévu, détection de l'alignement et révélation de
l'indication suivante.

== 5.3 Indice 3 — Assemblage de deux fragments

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Asset*], [*Spécification détaillée*], [*Outil*], [*Priorité*],
  [Fragment A], [Première partie de l'objet final ; forme conçue pour être rapprochée de l'autre fragment.], [Blender], [Indispensable],
  [Fragment B], [Deuxième partie complémentaire ; son contour doit correspondre au fragment A.], [Blender], [Indispensable],
  [Objet reconstitué], [Modèle complet obtenu après assemblage ; peut être un troisième modèle ou le résultat de l'alignement des deux parties.], [Blender / Unity], [Important],
  [Surfaces de raccord], [Faces de contact suffisamment cohérentes pour donner l'impression d'un objet unique.], [Blender], [Important],
  [Colliders], [Volumes de collision simples pour chaque fragment.], [Unity], [Indispensable],
  [Points d'assemblage], [Repères ou positions cibles utilisés pour détecter l'alignement.], [Unity], [Indispensable]
)

*Comportements associés à programmer dans Unity :* prise indépendante des
fragments, détection de proximité et d'orientation, alignement, assemblage
validé et affichage du code final.

= 6. Clavier et sortie virtuelle

#priority("Indispensable")
Ces éléments terminent la boucle de jeu. Ils peuvent être construits avec des
primitives et des composants Unity ; une modélisation Blender détaillée n'est
pas nécessaire.

== 6.1 Clavier virtuel

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Élément*], [*Contenu / rôle*], [*Outil conseillé*], [*Priorité*],
  [Base du clavier], [Panneau ou support qui regroupe les touches.], [Unity / Blender], [Indispensable],
  [Touches 0 à 9], [Dix boutons numériques interactifs.], [Unity UI / 3D], [Indispensable],
  [Afficheur], [Zone affichant les chiffres saisis ou des caractères masqués.], [Unity UI], [Important],
  [Bouton Valider], [Confirme le code saisi.], [Unity UI / 3D], [Indispensable],
  [Bouton Effacer], [Permet de corriger la saisie.], [Unity UI / 3D], [Important],
  [Retour visuel], [Indique une saisie acceptée ou refusée.], [Unity UI], [Important]
)

== 6.2 Sortie virtuelle

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Élément*], [*Contenu / rôle*], [*Outil conseillé*], [*Priorité*],
  [Porte ou portail], [Élément visuel représentant la sortie ; ne doit pas être confondu avec une porte physique à ouvrir.], [Unity / Blender], [Indispensable],
  [Cadre], [Contour visuel de la sortie si nécessaire.], [Blender / Unity], [Important],
  [État verrouillé], [Aspect initial avant validation du code.], [Unity], [Important],
  [État déverrouillé], [Aspect après validation du code.], [Unity], [Important],
  [Animation d'ouverture], [Animation ou transition visuelle déclenchée après validation.], [Unity], [Important],
  [Zone de victoire], [Zone logique qui valide la fin de partie lorsque les conditions sont réunies.], [Unity], [Indispensable]
)

= 7. Environnement réel, géométrie et mobilier

#priority("Indispensable")
La pièce existe physiquement. La géométrie fixe doit être récupérée en priorité
avec la Scene API et MRUK. Le scan détaillé avec ScanSpace est une amélioration,
pas une obligation du prototype minimal.

== 7.1 Architecture fixe

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Élément*], [*Représentation attendue*], [*Source / outil*], [*Priorité*],
  [Sol], [Surface de référence pour les déplacements et la navigation.], [Scene API / MRUK], [Indispensable],
  [Murs], [Plans ou volumes servant à l'occlusion et aux tests de ligne de vue.], [Scene API / MRUK], [Indispensable],
  [Coins et limites], [Géométrie permettant de délimiter la zone de jeu.], [Scene API / MRUK], [Indispensable],
  [Ouvertures], [Portes ou passages reconnus si disponibles et utiles à la scène.], [Scene API / MRUK], [Important],
  [Maillage détaillé de la pièce], [Modèle de la pièce exporté puis simplifié et recalé si le scan externe est retenu.], [ScanSpace / Blender], [Optionnel]
)

== 7.2 Mobilier mobile et obstacles

Les meubles mobiles ne doivent pas être intégrés définitivement au maillage
fixe. Le projet prévoit des volumes simplifiés dans Unity et un QR code associé
aux meubles suivis.

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Élément*], [*Représentation attendue*], [*Source / outil*], [*Priorité*],
  [Table réelle], [Volume simple (boîte ou collider) correspondant à la table physique.], [Unity], [Indispensable si utilisée],
  [Chaise réelle], [Volume simple correspondant à la chaise physique.], [Unity], [Indispensable si utilisée],
  [Autre meuble mobile], [Volume simplifié pour chaque meuble suivi par le système.], [Unity], [Selon le parcours],
  [QR code], [Marqueur imprimé de dimension connue, attaché ou placé sur le meuble.], [Générateur QR / impression], [Indispensable pour le suivi],
  [Repère du marqueur], [Point de référence et orientation utilisés pour estimer la pose du meuble.], [Unity], [Indispensable],
  [Obstacle de navigation], [Obstacle mis à jour lorsque la position du meuble est recalculée.], [Unity / NavMesh], [Indispensable]
)

*À ne pas modéliser inutilement :* les murs, le sol, les tables et les
chaises réels en version détaillée si la géométrie MRUK et les volumes Unity
suffisent. Les modèles décoratifs de mobilier ne remplacent pas les obstacles
physiques et ne doivent jamais créer une fausse zone praticable.

== 7.3 Calibration et ancrage

Il ne s'agit pas d'assets artistiques, mais de ressources et repères techniques
à préparer :

- Un repère spatial de référence pour la pièce.
- Des positions de référence pour les trois indices.
- Des ancrages spatiaux pour maintenir les objets virtuels en place.
- Des dimensions connues pour les marqueurs QR.
- Une procédure de vérification après déplacement d'un meuble.
- Un contrôle de recalage après déplacement du joueur et après redémarrage
  d'une session.

= 8. Interface et retours visuels

#priority("Important")
Les éléments d'interface peuvent être réalisés dans Unity. Ils ne nécessitent
pas nécessairement de maillage Blender.

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Élément*], [*Fonction*], [*Outil*], [*Priorité*],
  [Consigne courte], [Aide contextuelle lorsque l'interaction n'est pas évidente.], [Unity UI], [Important],
  [Indicateur de prise], [Retour visuel signalant qu'un objet peut être saisi.], [Unity], [Important],
  [Indicateur de sélection], [Montre quel objet est actuellement sélectionné.], [Unity], [Important],
  [Indicateur de progression], [Montre l'avancement des énigmes si cela est utile.], [Unity UI], [Optionnel],
  [Retour de code], [Signale code correct ou incorrect.], [Unity UI], [Important],
  [Écran de victoire], [Confirme la réussite de la partie.], [Unity UI], [Important],
  [Écran de défaite], [Confirme la capture par le monstre.], [Unity UI], [Important],
  [Indicateur de danger], [Alerte discrète lorsque le monstre est proche, si retenu dans le design.], [Unity UI], [Optionnel]
)

= 9. Effets visuels et éclairage

#priority("Important / optionnel")
Les effets doivent rester lisibles en passthrough et ne pas masquer la pièce
réelle. Il faut éviter les effets trop lumineux ou trop opaques qui gêneraient
la perception des obstacles physiques.

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Effet*], [*Usage*], [*Outil*], [*Priorité*],
  [Mise en évidence d'un indice], [Aide visuelle légère pour attirer l'attention sur un objet interactif.], [Unity], [Important],
  [Validation d'énigme], [Effet bref lorsque l'étape est réussie.], [Unity], [Important],
  [Déverrouillage], [Effet associé à l'activation de la sortie.], [Unity], [Important],
  [Capture], [Effet visuel bref associé à la défaite.], [Unity], [Important],
  [Particules], [Poussière, fumée ou apparition, uniquement si elles restent légères.], [Unity], [Optionnel],
  [Ambiance sombre], [Réduction volontaire de la visibilité ; à tester sans compromettre la sécurité.], [Unity], [Optionnel],
  [Lampe / lumière locale], [Source lumineuse virtuelle pour éclairer une petite zone.], [Unity], [Optionnel],
  [Transformation du monstre], [Modification ponctuelle de la silhouette avec blend shapes ou animation dédiée.], [Blender / Unity], [Optionnel],
  [Transformation du mobilier], [Habillage fantastique d'un meuble réel suivi, sans modifier son volume physique.], [Blender / Unity], [Optionnel]
)

= 10. Ressources audio

Les fichiers audio ne sont pas des modèles 3D. Ils doivent être récupérés,
enregistrés ou créés, puis intégrés dans Unity. L'équipe a repéré une banque
de sons d'horreur gratuite ; il faut vérifier la licence de chaque ressource
et conserver les informations d'attribution éventuelles.

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Ressource audio*], [*Déclencheur / usage*], [*Outil*], [*Priorité*],
  [Ambiance générale], [Fond sonore discret de la pièce.], [Fichier audio / Unity], [Important],
  [Pas du monstre], [Déplacement en patrouille et poursuite.], [Fichier audio / Unity], [Important],
  [Respiration], [Présence du monstre ou proximité du joueur.], [Fichier audio / Unity], [Optionnel],
  [Grognement], [Détection, recherche ou proximité.], [Fichier audio / Unity], [Important],
  [Attaque / capture], [Déclenchement de la défaite.], [Fichier audio / Unity], [Important],
  [Prise d'objet], [Saisie ou manipulation d'un indice.], [Fichier audio / Unity], [Optionnel],
  [Assemblage], [Réussite de la troisième énigme.], [Fichier audio / Unity], [Important],
  [Code accepté / refusé], [Validation du clavier virtuel.], [Fichier audio / Unity], [Important],
  [Déverrouillage], [Ouverture de la sortie virtuelle.], [Fichier audio / Unity], [Important],
  [Victoire], [Fin réussie de la partie.], [Fichier audio / Unity], [Important]
)

= 11. Extensions et objets supplémentaires

#priority("Optionnel")
Ces ressources ne doivent être commencées qu'après validation du parcours
minimal et de la navigation du monstre.

#table(
  columns: (1.35fr, 3.15fr, 1fr, 0.9fr),
  [*Asset*], [*Description / effet de jeu possible*], [*Outil*], [*Priorité*],
  [Lampe torche], [Objet tenu en main, avec modèle simple et point d'attache.], [Blender / Unity], [Optionnel],
  [Clé virtuelle], [Objet supplémentaire si une étape de progression est ajoutée.], [Blender / Unity], [Optionnel],
  [Objet distracteur], [Objet manipulable pouvant attirer l'attention du monstre.], [Blender / Unity], [Optionnel],
  [Objet ralentisseur], [Objet déclenchant un effet de ralentissement si cette mécanique est retenue.], [Blender / Unity], [Optionnel],
  [Décorations], [Petits accessoires virtuels qui enrichissent la scène sans encombrer la zone réelle.], [Blender / Unity], [Optionnel],
  [Couloir supplémentaire], [Extension spatiale après validation de la pièce initiale.], [MRUK / Unity], [Optionnel],
  [Pièce supplémentaire], [Nouvelle zone de jeu après validation du premier environnement.], [MRUK / Unity], [Optionnel]
)

= 12. Ce qui doit être modélisé dans Blender et ce qui ne doit pas l'être

#block(fill: pale-blue, radius: 5pt, inset: 9pt)[
  *À produire ou adapter dans Blender en priorité*

  - Le monstre complet, à partir du Goblin déjà téléchargé.
  - La préparation du squelette, du skinning et, si nécessaire, des corrections de maillage.
  - La plaque mystérieuse et son symbole.
  - Le disque gradué et son support éventuel.
  - Le fragment A et le fragment B.
  - L'objet final assemblé, seulement si un modèle distinct est utile.
  - Éventuellement le cadre ou l'apparence 3D de la sortie et du clavier si les primitives Unity ne suffisent pas.
]

#block(fill: pale-gold, radius: 5pt, inset: 9pt)[
  *À construire principalement dans Unity ou à récupérer autrement*

  - Les boutons du clavier, l'afficheur et les retours d'interface.
  - Les colliders, zones de préhension, pivots et points d'assemblage.
  - Les volumes simplifiés des meubles et les obstacles de navigation.
  - Les ancrages spatiaux, la calibration et les données de position.
  - Les QR codes à générer et à imprimer.
  - Les états de jeu, la FSM, le NavMesh et les transitions de l'Animator.
  - Les effets visuels simples et les sons.
]

*Règle de décision :* créer un modèle Blender uniquement lorsqu'une forme
spécifique apporte une valeur visuelle ou une interaction qui ne peut pas être
obtenue proprement avec les primitives et composants Unity.

= 13. Spécifications de livraison des modèles

Pour chaque modèle Blender destiné à Unity, vérifier les points suivants
avant de considérer l'asset comme terminé.

== 13.1 Géométrie

- Le modèle possède une forme lisible et adaptée à la distance d'observation.
- Les faces inutiles et détails invisibles sont limités.
- Les normales sont cohérentes.
- Les objets mobiles sont séparés lorsque leur mouvement doit être indépendant.
- Les pivots sont placés selon l'interaction attendue.
- Les transformations d'échelle et de rotation sont vérifiées avant export.

== 13.2 Matériaux et textures

- Les matériaux portent des noms explicites.
- Les textures nécessaires sont disponibles et correctement reliées.
- Les fichiers de texture sont conservés avec le projet.
- Les matériaux restent lisibles dans les conditions de passthrough.
- Les effets coûteux sont limités pour préserver les performances du Quest 3.

== 13.3 Collisions et interactions

- Le maillage visible est distinct du collider lorsque cela est utile.
- Les colliders des objets manipulables sont simples.
- Les objets ont une zone de préhension suffisamment grande.
- Les pivots et axes de rotation sont testés dans Unity.
- Les fragments disposent de repères d'assemblage cohérents.
- Les objets virtuels ne doivent pas encourager le joueur à toucher ou déplacer
  des objets physiques dangereux.

== 13.4 Export et intégration

- Format conseillé pour les modèles : FBX, selon les besoins du projet.
- Vérifier l'échelle et l'orientation après import dans Unity.
- Vérifier les matériaux et les textures après import.
- Pour le monstre, vérifier l'armature, le Skinned Mesh Renderer et les clips.
- Pour les objets, vérifier le Mesh Filter, le Mesh Renderer et les colliders.
- Tester sur le Quest 3 réel, et pas uniquement dans l'éditeur Unity.

= 14. Plan de production conseillé

L'ordre ci-dessous minimise le risque de fabriquer des éléments qui ne seront
pas utilisés. Les objets de l'escape game peuvent être développés en parallèle
de la préparation du monstre, mais les extensions restent secondaires.

#table(
  columns: (0.55fr, 2.25fr, 2.15fr, 1fr),
  [*Étape*], [*Travail*], [*Livrable vérifiable*], [*Priorité*],
  [1], [Auditer le Goblin téléchargé : ouverture du fichier, textures, rig, échelle et export FBX.], [Monstre importé dans Unity sans erreur majeure.], [Indispensable],
  [2], [Corriger le rig et le weight painting si nécessaire.], [Monstre testable avec plusieurs poses articulaires.], [Indispensable],
  [3], [Créer la plaque et son symbole.], [Plaque manipulable et orientable.], [Indispensable],
  [4], [Créer le disque gradué et son pivot.], [Disque rotatif avec repère fixe.], [Indispensable],
  [5], [Créer les deux fragments et définir leur assemblage.], [Fragments manipulables et assemblage détectable.], [Indispensable],
  [6], [Construire le clavier et la sortie dans Unity.], [Code saisissable et condition de victoire testable.], [Indispensable],
  [7], [Préparer les volumes de meubles et les QR codes nécessaires.], [Un meuble déplacé peut être repositionné virtuellement.], [Indispensable],
  [8], [Définir les clips, calibrer FreeMoCap et enregistrer marche et course.], [Deux captures exploitables.], [Indispensable],
  [9], [Nettoyer et retargeter les captures.], [Clips jouables sur le squelette du monstre.], [Indispensable],
  [10], [Ajouter recherche, attaque et transitions si la qualité le permet.], [États supplémentaires animés.], [Important],
  [11], [Ajouter les sons, effets et éléments décoratifs.], [Ambiance et retours plus complets.], [Important / optionnel],
  [12], [Envisager les extensions après validation.], [Couloir, objets bonus ou transformations.], [Optionnel]
)

= 15. Liste de suivi de l'équipe

Utiliser cette liste pendant la production. Remplacer « À faire » par
« En cours », « À tester » ou « Terminé » au fur et à mesure.

#table(
  columns: (0.55fr, 2.7fr, 1.05fr, 1.1fr),
  [*N°*], [*Tâche*], [*Responsable*], [*Statut*],
  [01], [Ouvrir et vérifier le modèle Goblin et ses fichiers associés.], [À définir], [À faire],
  [02], [Vérifier la licence et conserver la source du modèle Goblin.], [À définir], [À faire],
  [03], [Vérifier les textures et matériaux du monstre.], [À définir], [À faire],
  [04], [Vérifier le rig et la hiérarchie des os.], [À définir], [À faire],
  [05], [Corriger le weight painting si nécessaire.], [À définir], [À faire],
  [06], [Tester le FBX dans Unity.], [À définir], [À faire],
  [07], [Modéliser la plaque et son symbole.], [À définir], [À faire],
  [08], [Préparer le collider, le pivot et la prise de la plaque.], [À définir], [À faire],
  [09], [Modéliser le disque gradué.], [À définir], [À faire],
  [10], [Préparer l'axe de rotation et le repère fixe du disque.], [À définir], [À faire],
  [11], [Modéliser le fragment A.], [À définir], [À faire],
  [12], [Modéliser le fragment B.], [À définir], [À faire],
  [13], [Définir et tester l'assemblage des fragments.], [À définir], [À faire],
  [14], [Créer le clavier virtuel dans Unity.], [À définir], [À faire],
  [15], [Créer la sortie virtuelle et sa condition de victoire.], [À définir], [À faire],
  [16], [Préparer les volumes simplifiés des meubles retenus.], [À définir], [À faire],
  [17], [Générer, imprimer et tester les QR codes.], [À définir], [À faire],
  [18], [Définir les animations et transitions du monstre.], [À définir], [À faire],
  [19], [Calibrer FreeMoCap et enregistrer la marche.], [À définir], [À faire],
  [20], [Enregistrer la course.], [À définir], [À faire],
  [21], [Nettoyer et retargeter les animations.], [À définir], [À faire],
  [22], [Tester les animations dans Unity sur le Quest 3.], [À définir], [À faire],
  [23], [Ajouter les sons et retours visuels prioritaires.], [À définir], [À faire],
  [24], [Valider une partie complète gagnée et une partie perdue.], [À définir], [À faire]
)

= 16. Contrôle final avant la démonstration

#table(
  columns: (0.55fr, 4.25fr, 1fr),
  [*N°*], [*Point de contrôle*], [*Validation*],
  [1], [Le modèle du monstre est importé, correctement texturé et animé.], [À tester],
  [2], [Les articulations du monstre ne présentent pas de déformations bloquantes.], [À tester],
  [3], [La marche et la course issues de FreeMoCap sont déclenchées dans Unity.], [À tester],
  [4], [Les trois indices sont positionnés de façon cohérente dans la pièce.], [À tester],
  [5], [La plaque peut être saisie, tournée et examinée.], [À tester],
  [6], [Le disque peut être tourné et son alignement est reconnu.], [À tester],
  [7], [Les deux fragments peuvent être assemblés.], [À tester],
  [8], [Le code final peut être saisi sur le clavier virtuel.], [À tester],
  [9], [La sortie virtuelle valide la victoire.], [À tester],
  [10], [Le monstre patrouille et contourne les obstacles.], [À tester],
  [11], [Le monstre détecte le joueur uniquement si la ligne de vue est libre.], [À tester],
  [12], [Après perte de vue, le monstre recherche la dernière position connue.], [À tester],
  [13], [La capture déclenche la défaite sans contact physique.], [À tester],
  [14], [Le passthrough reste visible et la zone de déplacement est sûre.], [À tester],
  [15], [Les performances sont vérifiées sur le Quest 3 réel.], [À tester]
)

= 17. Décisions à confirmer par l'équipe

Les points suivants ne sont pas entièrement spécifiés dans la proposition
initiale. Ils doivent être décidés avant de finaliser les modèles concernés :

- Le design visuel définitif du monstre : conserver le Goblin téléchargé ou
  choisir un autre personnage.
- La forme, les dimensions et le style artistique de la plaque.
- Le symbole exact à graver sur la plaque.
- Le nombre et le type de graduations et de symboles du disque.
- La forme de l'objet final obtenu par assemblage.
- Le style du clavier et de la sortie virtuelle.
- Le nombre exact de meubles à suivre par QR code.
- Les animations supplémentaires à enregistrer au-delà de la marche et de la
  course.
- Les effets visuels et sons qui seront conservés dans le prototype final.

#v(8pt)
#line(length: 100%, stroke: 1pt + accent)
#align(center)[
  #text(size: 8pt, fill: luma(95))[TOHANNIC : NO WAY OUT — Inventaire de production des assets]
  #text(size: 8pt, fill: luma(95))[Document de travail de l'équipe — INF3001 / INF3002]
]

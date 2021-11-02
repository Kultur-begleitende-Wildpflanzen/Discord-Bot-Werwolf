class Texte():
    # Texte
    werwolftext = 'Wie viele Werwölfe soll es geben? (Vorschlag: {})'
    specialText = 'Welche special Werwölfe soll es geben? (Reagiere mit dem entsprechenden Emoji) \n :skull_crossbones: = Weißer Werwolf \t :child: = Wildes Kind \n :baby: = Wolfsbaby \t :older_man: = Urwolf'
    seeingText = 'Welche Charaktere mit seherischen Fähigkeiten soll es geben? (Reagiere mit dem entsprechenden Emoji) \n :bear: = Bärenführer \t :fox: = Fuchs \n :crystal_ball: = Seherin'
    dyingText = 'Welche mordlustigen Charaktere soll es geben? (Reagiere mit dem entsprechenden Emoji) \n :boar: = Jäger \t :syringe: = Tetanusritter \n :bomb: = Terrorist'
    oneHitText = 'Welche One-Hit-Wonder Charaktere soll es geben? (Reagiere mit dem entsprechenden Emoji) \n :smiling_face_with_3_hearts: = Amor \t :printer: = Kopierertyp \n :baby_symbol: = Ergebene Magd'
    restText = 'Welche zusätzlichen Charaktere soll es geben? (Reagiere mit dem entsprechenden Emoji) \n :kiss: = Nutte \t :levitate: = Leibwächter \n :elf: = Reine Seele \t :scales: = Stotternder Richter \n :angel: = Engel \t :mage:  = Hexe'

    help_text = 'Dieser Hilfstext muss noch geschrieben werden.'
    game_start_text = 'Neues Werwolfspiel wird gestartet.'
    game_join_text = 'Wenn du mitspielen möchtest, reagiere mit :thumbsup:'
    game_end_text = 'Das Werwolfspiel wird beendet. Alle Kanäle und Rollen werden entfernt'
    game_clear_text = 'Chat wird gelöscht!'
    game_player_role_count_text = 'Bitte wähle die Rollen aus, mit denen ihr spielen wollt. \nAnzahl der Mitspieler: {} \n**Anzahl der ausgewählten Rollen: {}**'
    game_end_safety_question_text = 'Bist du sicher, dass du das Spiel beenden willst? Alle Channel werden dadurch gelöscht und Spieler die sich noch in diesen Channels befinden, werden disconnected. \n :white_check_mark: Ja \t :x: Nein \n'

    # Erzähler
    erzaehler_commands_text = '**!start game**...\n**!start menu**...\n**!zusammenfassung**: gibt dir eine Zusammenfassung der noch lebenden Spieler, Rollen und deren Fähigkeiten \n**!vorschlag**: gibt dir einen Vorschlag, was du in der Nacht zu den einzelnen Rollen sagen könntest'

    # Emojis
    werwolfEmojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    specialEmojis = ["☠", "🧒", "👶", "👴"]
    seeingEmojis = ["🐻", "🦊", "🔮"]
    dyingEmojis = ["🐗", "💉", "💣"]
    oneHitEmojis = ["🥰", "🖨", "🚼"]
    restEmojis = ["💋", "🕴", "🧝", "⚖", "👼", "🧙"]
    ynemojis = ["✅", "❌"]

    # dictionarys
    characterdict = {
        "werwolf": 0,  # 9
        "werwolf_weißer": 0,  # 12
        "wildes_kind": 0,  # 2
        "werwolf_baby": 0,  # Gar nicht
        "werwolf_ur": 0,  # 10
        "bärenführer": 0,  # Gar nicht
        "fuchs": 0,  # 5
        "seherin": 0,  # 4
        "jäger": 0,  # Gar nicht
        "tetanusritter": 0,  # Gar nicht
        "terrorist": 0,  # Gar nicht
        "amor": 0,  # 3
        "kopierertyp": 0,  # 1
        "magd": 0,  # Gar nicht
        "nutte": 0,  # 7
        "leibwächter": 0,  # 6
        "reine_seele": 0,
        "richter": 0,  # 8
        "engel": 0,  # Gar nicht
        "hexe": 0,  # 11
        "dorfbewohner": 0  # Gar nicht
    }
    emojidict = {
        "1️⃣": ["werwolf"],
        '2️⃣': ["werwolf", "werwolf"],
        '3️⃣': ["werwolf", "werwolf", "werwolf"],
        '4️⃣': ["werwolf", "werwolf", "werwolf", "werwolf"],
        '5️⃣': ["werwolf", "werwolf", "werwolf", "werwolf", "werwolf"],
        "☠": "werwolf_weißer",
        "🧒": "wildes_kind",
        "👶": "werwolf_baby",
        "👴": "werwolf_ur",
        "🐻": "bärenführer",
        "🦊": "fuchs",
        "🔮": "seherin",
        "🐗": "jäger",
        "💉": "tetanusritter",
        "💣": "terrorist",
        "🥰": "amor",
        "🖨": "kopierertyp",
        "🚼": "magd",
        "💋": "nutte",
        "🕴": "leibwächter",
        "🧝": "reine_seele",
        "⚖": "richter",
        "👼": "engel",
        "🧙": "hexe"
    }
    emojidict_id = {
        "1️⃣": [1],
        '2️⃣': [1, 1],
        '3️⃣': [1, 1, 1],
        '4️⃣': [1, 1, 1, 1],
        '5️⃣': [1, 1, 1, 1, 1],
        "☠": '2',
        "🧒": '3',
        "👶": '4',
        "👴": '5',
        "🐻": '6',
        "🦊": '7',
        "🔮": '8',
        "🐗": '9',
        "💉": '10',
        "💣": '11',
        "🥰": '12',
        "🖨": '13',
        "🚼": '14',
        "💋": '15',
        "🕴": '16',
        "🧝": '17',
        "⚖": '18',
        "👼": '19',
        "🧙": '20'
    }
    namedict = {
        "werwolf_weißer": "Weißer Werwolf",
        "wildes_kind": "Wildes Kind",
        "werwolf_baby": "Wolfsbaby",
        "werwolf_ur": "Urwolf",
        "bärenführer": "Bärenführer",
        "fuchs": "Fuchs",
        "seherin": "Seherin",
        "jäger": "Jäger",
        "tetanusritter": "Tetanusritter",
        "terrorist": "Terrorist",
        "amor": "Amor",
        "kopierertyp": "Kopierertyp",
        "magd": "Ergebene Magd",
        "nutte": "Nutte",
        "leibwächter": "Leibwächter",
        "reine_seele": "Reine Seele",
        "richter": "Stotternder Richter",
        "engel": "Engel",
        "hexe": "Hexe"
    }
    textdict = {
      # Rollen Texte- Nachricht an Personen
        "werwolf": "Du bist Werwolf! \nDu gewinnst, sobald der letzte Dorfbewohner gestorben ist und somit nur noch die Werwölfe leben. \nAm Tag versuchst du unauffällig zu sein und Verdächtigungen von dir abzulenken. Während der Nacht wachst du jedoch auf, um mit deinem Rudel ein Opfer aus der Nachbarschaft zu zerfleischen. \nGuten Appetit!",
        "werwolf_weißer": "Du bist der Große, Weiße Werwolf! \nDu gewinnst, sobald alle haarigen und nicht-haarigen Dorfbewohner gestorben sind. Richtig gelesen, du gewinnst nur alleine! \nAm Tag versuchst du unauffällig zu sein und Verdächtigungen von dir abzulenken. Während der Nacht wachst du jedoch auf, um mit deinem Rudel ein Opfer aus der Nachbarschaft zu zerfleischen. \nDa dies deinen Appetit noch lange nicht stillt, wachst du jede Nacht ein weiteres Mal auf um ein zweites Opfer zu reißen. \nDoch aufgepasst, dein Wolfsrudel darf keinen Verdacht schöpfen!",
        "wildes_kind": "Du bist das Wilde Kind! \nDa Vorbilder essenziell in deiner Entwicklung sind, wählst du in der ersten Nacht ein solches aus. Solange dein Vorbild lebt, spielst du auf Seiten der Dorfbewohner. \nWird dein Vorbild aber umgebracht, wirst du von deiner Trauer überwältigt und verwandelst dich in einen Werwolf. Falls dies passiert, arbeitest du mit den Werwölfen darauf hin, das Dorf auszulöschen. \nAlso mach dich auf pubertäre Stimmungsschwankungen gefasst!",
        "werwolf_baby": "Du bist das Werwolfsbaby! \nDu gewinnst, sobald der letzte Dorfbewohner gestorben ist und somit nur noch die Werwölfe leben. \nAm Tag versuchst du unauffällig zu sein und Verdächtigungen von dir abzulenken. Während der Nacht wachst du jedoch auf, um mit deinem Rudel ein Opfer aus der Nachbarschaft zu zerfleischen. \nDu genießt als Welpe eine ganz besondere Stellung in deinem Rudel: Wenn du getötet wirst, gerät dein Rudel in Rage und tötet in der nächsten Nacht zwei Bewohner. Welcher Mensch tötet denn auch bitte unschuldige Welpen?!",
        "werwolf_ur": "Du bist der Urwolf! \nDu gewinnst, sobald der letzte Dorfbewohner gestorben ist und somit nur noch die Werwölfe leben. \nAm Tag versuchst du unauffällig zu sein und Verdächtigungen von dir abzulenken, Während der Nacht wachst du jedoch auf, um zusammen mit deinem Rudel ein Opfer aus der Nachbarschaft zu zerfleischen. \nEinmalig kannst du ein Opfer infizieren um es nicht zu verspeisen, sondern das Opfer zu einem Werwolf machen. Also, erst denken, dann futtern!",
        "bärenführer": "Du bist der Bärenführer! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nDein Bär kann die Werwölfe erschnüffeln und wird unruhig, wenn er welche wittert. Er brummt laut, wenn ein Werwolf unter den lebenden Spielern ist, die direkt über und unter dir sind. \nSei also wachsam in den frühen Morgenstunden und lausche, ob dein Bär dir ein Zeichen schickt.",
        "fuchs": "Du bist der Fuchs! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nAls Fuchs kannst du nachts eine Gruppe von drei benachbarten Spielern beobachten und herausfinden, ob unter ihnen mindestens ein Werwolf ist. \nSehr präzise sind deine Beobachtungen jedoch nicht und sobald du eine Gruppe ohne Werwölfe beobachtest, verlierst du deine Neugier. \nAlso spitz die Nase und bleib achtsam!",
        "seherin": "Du bist die Seherin! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nJede Nacht überkommen dich Visionen und du siehst die Identität einer von dir erwählten Person. \nAlso schärfe deinen siebten Sinn und trage zur Rettung deines Dorfes bei!",
        "jäger": "Du bist der Jäger! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch die Dorfbewohner leben. \nWährend deines Lebens bist du nur ein langweiliger, grummeliger Dorfbewohner. Sobald du aber getötet wirst, holst du mit letzter Kraft dein altes Jagdgewehr hervor und richtest den Lauf auf einen von dir Verdächtigten. \nDenn eins ist dir klar, für deinen Tod muss jemand bestraft werden!",
        "tetanusritter": "Du bist der Tetanusritter! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch die Dorfbewohner leben. \nDu lebst mit deiner treuen Stute und deinem rostigen Schwert nun schon seit Jahren im Dorf und hast dich dort zur Ruhe gesetzt. \nFalls du von dem Werwolfsrudel angegriffen wirst, kannst du dein Leben zwar nicht verteidigen, aber du triffst mit deinem rostigen Schwert den nächsten Werwolf unter dir. Dieser stirbt in der darauffolgenden Nacht an seinen Wunden.",
        "terrorist": "Du bist der Terrorist! \nDu kannst dich einmalig mit *!boom @[**Username**]* in die Luft sprengen \nDu kannst deinen Sprenggürtel zu jeder Zeit und in der Nähe einer Person deiner Wahl zünden. \nDein Spielziel? Chaos und Verwüstung.",
        "amor": "Du bist Amor! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nAls Vertreter der Liebe verkuppelst du in der ersten Nacht zwei Liebende, die daraufhin nicht mehr ohne einander leben wollen. Sie leben zusammen- und gehen zusammmen. Denn wenn einer stirbt, vergeht der andere an seinem gebrochenen Herzen. \nAlso spann deinen Bogen und zerstöre Leben!",
        "kopierertyp": "Du bist der Kopierertyp! \nAufgrund einer schweren Kindheit hast du Angst, dein wahres Ich zu zeigen. \nDu bist neu im Dorf und willst, dass die anderen dich mögen. \nDir ist jemand aufgefallen, den alle zu mögen scheinen. Das ist die Lösung! So zu sein, sichert dir bestimmt die Zuneigung des Dorfes. \nDoch sei vorsichtig. Wenn du unwissentlich einen Werwolf wählst, wirst du ein Teil des Rudels und dein Durst nach Menschenblut erwacht!",
        "magd": "Du bist die ergebene Magd! \nDu führst ein ruhiges, fast schon langweiliges Leben als normale Dorfbewohnerin. Somit gewinnst du, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nDoch dies kann sich schlagartig ändern! \nAuf der Beerdigung eines verstorbenen Mitbürgers spürst du plötzlich eine geheimnisvolle Kraft: Die Fähigkeiten des Verstorbenen sind auf dich übergegangen! \nVon nun an bist du eine komplett neue Persönlichkeit und handelst so, wie es der Verstorbene getan hätte. \nDoch wann in der perfekte Zeitpunkt? Das liegt ganz alleine in deinem Ermessen.",
        "nutte": "Du bist ne Nutte! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nIm Gegensatz zu anderen Personen in deinem Dorf (*räusper Tetanusritter) bist du noch nicht im Ruhestand un musst dir deinen Lebensunterhalt mit ehrlicher Arbeit verdienen. \nDeshalb besuchst du jede Nacht einen von dir erwählten Kunden. Ob du Stammkunden hast oder nicht, ist dabei ganz und gar deine Entscheidung! \nDein Beruf hat aber einen ganz offensichtlichen Vorteil: Wer nicht zu Hause ist, kann dort auch nicht von den Werwölfen erwischt werden. Wenn aber die Werwölfe in das Haus deines Kunden eindringen...",
        "leibwächter": "Du bist der Leibwächter! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nDu leidest an einem krankhaften Helfersyndrom und damit verbundenen Schlafstörungen. Daher wachst du jede Nacht vor der Tür eines anderen Dorfbewohners. \nSollten die Bewohner Opfer eines Werwolfangriffs werden, lieferst du dir einen Kampf mit dem gesamten Rudel. Du kannst die Werwölfe zwar in die Flucht schlagen, doch erliegst selbst in der selben Nacht noch deinen Verletzungen. \nDurch die Erfüllung deiner Bestimmung kannst du aber in Frieden sterben.",
        "reine_seele": "Du bist die Reine Seele! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nWie kein Anderer bist du ein offenes Buch für deine Mitmenschen. Wer dich auch nur ansieht, merkt, dass du nichts Böses im Schilde führen kannst. \nAlso nutze deine Unschuld, um während der Dorfversammlung die Schuldigen zu entlarven!",
        "richter": "Du bist der stotternde Richter! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nWie der pflichtbewusste Bürger der du bist, beginnst du mit deiner Arbeit schon im Morgengrauen. \nDoch leider scheint dir niemand hier im Dorf eine Hilfe sein zu wollen. Ständig wirst du unterbrochen. \nZum Glück hast du als Richter die Befugnis, jeden Tag einen Bürger verstummen zu lassen. Diese einstweilige Verfügung gilt zwar nur für einen Tag, jedoch kannst du jeden Morgen einen neuen Bürger verstummen lassen. \nAlso nutze deine Fähigkeit zum Wohle aller.",
        "engel": "Du bist der Engel! \nDu gewinnst einzig und allein, wenn du in der ersten Runde stirbst. \nDir gefällt es unter den Menschen nicht besonders und du möchtest nichts anderes, als raus aus diesem abgeschotteten Dorf mit seinen schrulligen Einwohnern. \nJeder weitere Tag ist wie die leckende Zungen des Höllenfeuers unter deinen Fußsohlen. \nAch, wie sehr du dich nach den reich gedeckten Tafeln deines Heimatortes sehst!",
        "hexe": "Du bist die Hexe! \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nDu kennst die Bewohner des Dorfes ebenso gut, wie die Kräuter in deinen Regalen. \nDeswegen kannst du Dorfbewohner wiederbeleben, wenn sie von den Werwölfen getötet wurden. Oder du kannst, wenn du es für nötig hältst, auch jemanden töten. \nDoch pass auf! Beide Tränke brauchen Zeit zum Brauen und du kannst sie jeweils nur einmal verwenden. Also handle mit Bedacht!",
        "dorfbewohner": "Du bist normal. \nDu gewinnst, sobald der letzte Werwolf gestorben ist und somit nur noch Dorfbewohner leben. \nDoch wie du in dieses Dorf gekommen bist? Du weißt es nicht. \nManchmal denkst du, du bist in einem Spiel gelandet. Die Leute hier sind so seltsam, dass sie unmöglich echt sind, richtig? \nAber hey. Spiele sind da um gespielt zu werden. Und du bist hier, um zu gewinnen. \nAlso halt die Ohren steif und setz deine Wahlstimme richtig ein. Denn sie ist alles was du hast.",
        "liebespaar_1": "Du bist verliebt! \nOh wie schön die Welt plötzlich ist. Alles rosarot, kein Übel mehr. Aber du siehst im Grunde eh nichts anderes als dein Herzblatt. \nDein Ziel ist es, nur mit deinem Sonnenschein zu überleben. Also pack die Waffen aus, denn im Krieg und der Liebe ist alles erlaubt. \nAber pass auf, denn ohne Romeo gibt es auch keine Julia. Sobald der eine stirbt, erlischt auch das Lebenslicht des Anderen.",
        "liebespaar_2": "Du bist auf ewig mit {} verbunden.",
        "infizierter": "Du wurdest vom Urwolf infiziert! \nDamit bist du jetzt ein Werwolf und gewinnst, sobald der letzte Dorfbewohner gestorben ist und somit nur noch die Werwölfe leben. \nTrotz all dieser Veränderung bleibst du deiner bisherigen Bestimmung treu und führst weiterhin deine Aufgaben und Pflichten aus."
    }

    commontextdict = {
        # Rollen Texte- Erklärung (für rollenübersicht)
        "werwolf": "Werwölfe spielen im Team und haben das Ziel, alle Dorfbewohner zu fressen.",
        "werwolf_weißer": "Der Große Weiße Werwolf tarnt sich als normaler Wolf, kann aber pro Nacht noch eine weitere Person fressen. Egal ob Wolf oder Nicht-Wolf.",
        "wildes_kind": "Das Wilde Kind wählt in der ersten Nacht ein Vorbild. Es ist so lange Dorfbewohner, bis sein Vorbild stirbt. Passiert dies, mutiert das Wilde Kind zum Werwolf.",
        "werwolf_baby": "Das Werwolfbaby stimmt wie die anderen Werwölfe über das Opfer ab. Stirbt es aber, töten die Werwölfe in der nächsten Nacht zwei Dorfbewohner.",
        "werwolf_ur": "Der Urwolf hat die Fähigkeit, ein Opfer in einen Werwolf zu verwandeln. Wen er wann verwandeln will, ist ihm überlassen.",
        "bärenführer": "Der Bärenführer führt seinen Bär, der Werwölfe in seiner Nähe wittert. Wenn einer der beiden Nachbarn Werwolf ist, brummt der Bär am Ende der Nacht. Leere Häuser oder tote Sitznachbarn werden hierbei ausgelassen.",
        "fuchs": "Der Fuchs kann jede Nacht die Aura dreier nebeneinander sitzenden Personen erkennen. Findet er einmal eine Personengruppe ohne Werwolf, erlischt seine Fähigkeit.",
        "seherin": "Die Seherin erfährt jede Nacht die Identität einer Person ihrer Wahl.",
        "jäger": "Wird der Jäger getötet, reißt er eine weitere Person mit in den Tod.",
        "tetanusritter": "Der Tetanusritter wehrt sich bei einem Angriff der Werwölfe. Der nächste Werwolf unter ihm stirbt in der darauffolgenden Nacht.",
        "terrorist": "Der Terrorist kann sich zu einem frei gewählten Zeitpunkt in die Luft sprengen und nimmt dabei einen weiteren Dorfbewohner mit sich.",
        "amor": "Amor verkuppelt in der ersten Nacht zwei Liebende, welche fortan das neue Spielziel haben, nur zu zweit zu überleben. Wird einer getötet, stirbt auch der Andere.",
        "kopierertyp": "Der Kopierertyp kopiert am Anfang die Rolle einer anderen Person. Er könnte also sowohl auf Seiten der Dorfbewohner stehen, als auch mit den Werwölfen spielen.",
        "magd": "Die Ergebene Magd kann, sobald sie will, die ihr bis dahin unbekannte Rolle eines verstorbenen Mitspielers annehmen.",
        "nutte": "Die Nutte übernachtet jede Nacht in einem anderen Haus. Bedeutet: Sie kann nicht zu Hause getötet werden. Falls die Werwölfe jedoch ihren Kunden fressen, stirbt sie ebenfalls.",
        "leibwächter": "Der Bodyguard kann sich jede Nacht einen neuen Schützling aussuchen. Er schützt dessen Haus und stirbt, wenn er gegen die Werwölfe kämpfen muss.",
        "reine_seele": "Bei der Reinen Seele ist von Anfang an allen bekannt, dass sie ein unschuldiger Dorfbewohner ist.",
        "richter": "Der Stotternde Richter kann jede Nacht eine Person zum Verstummen bringen, welche für die Runde nicht sprechen oder wählen darf. Es darf nicht zweimal hintereinander die gleiche Person gewählt werden.",
        "engel": "Der Engel gewinnt, wenn er in der ersten Runde stirbt. Er richtet seine gesammte Spielweise darauf aus.",
        "hexe": "Die Hexe hat einen Heilungs- und einen Tötungstrank, die sie während der Nacht einsetzen kann.",
        "dorfbewohner": "Normalos haben keine besonderen Fähigkeiten."
    }
    storydict = {
        # Vorschläge für den Erzähler
        "nacht": "Es wird Dunkel im Düsterwald. Stille legt sich über das Dorf und alle Bewohner schlafen ein.",
        "kopierertyp": "Doch ein Dorfbewohner kann nicht schlafen. Der Kopierertyp ist neu im Dorf und ist sich unsicher, wie er die anderen am besten von sich überzeugen kann. Weil er seinen eigenen Charakter dafür nicht ausreichend findet, sucht er sich einen Nachbarn, wessen Fähigkeiten er kopiert, um so das Dorf von sich zu überzeugen.\nKopierertyp, wessen Fähigkeit möchtest du kopieren?\nDer Kopierertyp hat seine neue Identität angenommen und schläft wieder ein.",
        "amor": "Der nächste nachtaktive Charakter ist Amor. Amor hat sich zum Ziel gesetzt, Liebe und Leidenschaft unter die Menschheit zu bringen. Deshalb spannt er seinen Bogen und schießt seine Liebespfeile auf zwei Personen, die fortan nicht mehr ohne einander leben können.\nAmor, wen möchtest du verkuppeln?\nAmor hat seine Pfeile verschossen und schläft wieder ein.\nDas Liebespaar erwacht, verliebt sich unsterblich ineinander und verbringt einige wunderschöne Stunden miteinander. Sie schlafen von ihrem Liebesglück erfüllt wieder ein.",
        "leibwächter": "Der Leibwächter wälzt sich in seinem Bett hin und her und kann nicht einschlafen. Er kann einfach nicht damit leben, dass seine Nachbarn ungeschützt Werwolfangriffen ausgesetzt sind. Deshalb zieht er sich schnell eine Jacke über und stellt sich, Wache haltend, vor das Haus eines Nachbars. Hier wird er keinen einzigen Werwolf durchlassen, auch wenn er dafür sein eigenes Leben geben muss.\nLeibwächter, vor welcher Tür willst du diese Nacht wachen?\nDer Leibwächter hat sich vor eine Tür gestellt und die Nacht geht weiter.",
        "nutte": "Die Nutte macht sich zum Ausgehen bereit. Aufgrund ihrer unvergleichlichen Fähigkeiten ist sie im Dorf hoch angesehen und zählt zahlreiche Dorfbewohner zu ihrer Kundschaft. Das Geschäft floriert und Anfragen hat sie genug. Trotz der Gefahr zieht sie also ihren Mantel an und tritt in die Nacht.\nNutte, wen möchtest du diese Nacht beglücken?\nDie Nutte ist bei ihrem Kunden angekommen und verbringt mit ihm eine wilde Nacht.",
        "fuchs": "Der Magen knurrt und ihre Jungen verlangen nach etwas zu essen. Die Fähe beschließt auf Futtersuche zu gehen, um die hungrigen Mäuler zu stopfen. Aber warte! Was riecht sie da? Ist es ein Werwolf? Oder doch nur der Hund eines Dorfbewohners?\nFuchs, an welchem Haus möchtest du in dieser Nacht vorbei laufen?\nDie Fähe hat ihre Jungen gefüttert und verschwindet in den tiefen des Waldes.",
        "seherin": "Karten rascheln durcheinander und schillernde Rauchschwaden schweben im Spiegel. Die Luft vibriert vor Magie und Macht und die Seherin sitzt konzentriert vor ihrer Zauberkugel. Dass es Werwölfe unter den Dorfbewohnern gibt, weiß sie schon lange, aber bisher konnte sie nie einen identifizieren. Vielleicht wird sie ja heute mehr Glück haben?\nSeherin, wessen Identität möchtest du heute erfahren?\nDie Seherin fällt, von ihrer Eingebung erfüllt, in einen tiefen Schlaf.",
        "wildes_kind": "Ein strubbeliger Kopf schiebt sich aus dem Scheunentor. Sieht es jemand? Nein, nur rabenschwarze Nacht umgibt das Wilde Kind, als es sich auf die Suche nach etwas Essbaren macht. Es stolpert die Straßen entlang, getrieben von Hunger, als sich plötzlich eine Tür öffnet. \"Kind, du wirst dich noch erkälten! Komm herein in die gute Stube.\" So gut wie in dieser Nacht hatte es lange nicht mehr gegessen und das wilde Kind beschloss, dass dieser Dorfbewohner für immer sein liebster sein würde.\nWildes Kind, wen wählst du als dein Vorbild?\nDas Wilde Kind hat sein Vorbild gewählt und schlummert wieder in seine diffusen Träume.",
        "werwolf_1": "Ein Magen knurrt. Kurz darauf ertönt ein leises Jaulen. Die Werwölfe haben schon seit Ewigkeiten nichts mehr gefressen. Da der Morgen schon dämmert, haben sie auch nicht mehr viel Zeit zum Jagen. Ihr Hunger überwältigt die Werwölfe und sie machen sich, getrieben von ihren Instinkten, auf in Richtung Dorf.\nWerwölfe, wen möchtet ihr heute fressen?",
        "werwolf_ur": "Doch halt! Ein Schatten schiebt sich über das Opfer, welches nur noch schwach atmet. Der älteste und weiseste Wolf tritt vor sein Rudel. Er schnuppert an dem Opfer. Lohnt es sich vielleicht für diese eine Nacht auf einen vollen Magen zu verzichten? Wäre das Opfer stark genug, um zu einem von ihnen zu werden?\nUrwolf, möchtest du das Opfer infizieren?",
        "werwolf_2": "Die Werwölfe schlafen wieder ein. Müde von der aufregenden nächtlichen Jagd, haben sie sich wieder in ihr menschliches Ich verwandelt und liegen zufrieden träumend in ihren Kojen. ",
        "werwolf_weisser": "Doch ein Werwolf treibt sich immer noch durch die Gassen von Düsterwald. Der Große Weiße Werwolf ist noch nicht satt. Wer wird sein Opfer? Ist es ein weiterer Dorfbewohner? Oder ist etwa ein Werwolf in seiner Ungnade gefallen?\nGroßer Weißer Werwolf, wen möchtest du heute fressen?\nNun ist auch endlich der Hunger des Großen Weißen Werwolfs gestillt und er schläft, in einen Menschen verwandelt, wieder ein.",
        "hexe": "Was riecht denn hier so gut? Es sind sicherlich die frisch gepflückten Kräuter, die nur ihre volle Wirkung entfalten, wenn sie um genau 4:44 Uhr in der Nacht gepflückt werden. Doch als sie in ihr kleines Häuschen am Waldesrand zurückkehrt, läuft ihr ein eiskalter Schauer über den Rücken. Ihre Kristallkugel leuchtet blutrot auf. Die Hexe erschaudert, denn sie weiß, was das bedeutet. Es gab einen Mord!\nHexe, möchtest du das Opfer, heilen?\nHexe, möchtest du jemanden töten?\nEtwas benebelt von den Gerüchen der starken Kräutern nickt die Hexe wieder ein.",
        "richter": "Die Sonne geht langsam auf und die Amseln tanzen zwitschernd über die Dächer. Doch ein Dorfbewohner sitzt schon lange in seinem Büro. Der Richter hat viel zu tun und bearbeitet Anfrage um Anfrage. Doch andauernd kommt dieser eine Dorfbewohner und stört ihn bei seiner wichtigen Arbeit. Er kann es nicht fassen! In seiner Wut verfasst er einen Antrag: Aus dem Mund dieses Dorfbewohners kommt doch eh nichts Nützliches, warum sollte er dann am nächsten Tag sprechen dürfen?\nStotternder Richter, welche Person darf heute nicht sprechen?",
        "magd":"Die Dämmerung schreitet voran und eine kleine Trauergesellschaft findet sich auf dem Friedhof ein. Tief betroffen von dem Unglück der Nacht, halten sie sich in den Armen.\nDer Abschied fällt schwer, weswegen sie nicht bemerken, wie der ergebenen Magd ein Schauer durch den gesamten Körper fährt. Es scheint, als würden die Kräfte, die das Dorf in der Nacht zuvor verloren hat, von ihr Besitz ergreifen wollen.\nWird die Magd diesen Kräften widerstehen können?",
        "tag": "Von trillernden Pinguinen, Flamingos und Wanderfalken geweckt, erwacht das ganze Dorf Düsterwald zum Leben."
    }
    confirmmenudict={
        "many": 'Es wurden zu viele Rollen ausgewählt. Bitte wähle erneut. \nAnzahl Spieler: {} \nAnzahl Rollen: {} \n' ,
        "perfect": 'Wenn du mit der Auswahl zufrieden bist, bestätige deine Auswahl mit \n :white_check_mark: Ja \t :x: Nein \n',
        "less": 'Es wurden weniger Rollen als Mitspieler gewählt. Die Rollen werden automatisch durch Dorfbewohner aufgefüllt. Bist du mit der Auswahl der Rollen zu frieden dann bestätige mit \n :white_check_mark: Ja \t :x: Nein \n',
        "divider": '\n-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
    }

    deathtextdict_day = {
        #"Erster_Text":'{Playername} wurde getötet. Er war {Role}.',
        "Zweiter_Text":'Die Leiche von {Playername} baumelt am Galgen. Der Gehängte war {Role}.',
        "Dritter_Text":'Der Kopf von {Playername} rollt den Marktplatz entlang. Verdient als {Role}!',
        "Vierter_Text":'Die Türen schließen sich um {Playername}, möge {Role} nun für ewig in der eisernen Jungfrau verrotten.',
        #"Fünfter_Text":'Seht! Da weht {Playername} gemächlich am Baum hängend vor sich hin. {Role} sieht so aus, als hätte {Role} da schon immer hingehört.',
        "Sechster_Text":'Wir haben einen schönen Behälter für {Playername} gefunden! Darin soll {Role} für eine laaange Zeit leben.',
        "Siebter_Text":'Man sagte immer, {Playername} wäre zu nichts zu gebrauchen. {Role} macht sich aber herrlich als Vogelscheuche!',
        "Achter_Text":'Noch sind die Wetten offen! Wie lange werden die süßen Nager brauchen um durch {Playername} der Hitze zu entkommen? Hoffen wir, dass {Role} das Glück beiseite steht!'
    }
    pairtextdict={
        "Todestext":'_"So? Kommet jemand? So will ich´s kurz machen. O glüklicher Dolch! hier ist deine __Scheide__, hier roste und laß mich sterben."_ (Romeo und Julia, 5. Aufzug, 4. Szene)\nOhne einander wollten sie nicht leben. {partner} unsere Julia hat sich wegen des Todes ihres Romeos {victim} erdolcht. Das Dorf muss also auf {Role} verzichten.\nMöget ihr für immer beieinander ruhen!'
    }

    deathtextdict_night = {
        #"Erster_Text":'{Playername} wurde getötet. Er war {Role}.',
        "Zweiter_Text":'N Die Leiche von {Playername} baumelt am Galgen. Der Gehängte war {Role}.',
        "Dritter_Text":'N Der Kopf von {Playername} rollt den Marktplatz entlang. Verdient als {Role}!',
        "Vierter_Text":'N Die Türen schließen sich um {Playername}, möge {Role} nun für ewig in der eisernen Jungfrau verrotten.',
        #"Fünfter_Text":'Seht! Da weht {Playername} gemächlich am Baum hängend vor sich hin. {Role} sieht so aus, als hätte {Role} da schon immer hingehört.',
        "Sechster_Text":'N Wir haben einen schönen Behälter für {Playername} gefunden! Darin soll {Role} für eine laaange Zeit leben.',
        "Siebter_Text":'N Man sagte immer, {Playername} wäre zu nichts zu gebrauchen. {Role} macht sich aber herrlich als Vogelscheuche!',
        "Achter_Text":'N Noch sind die Wetten offen! Wie lange werden die süßen Nager brauchen um durch {Playername} der Hitze zu entkommen? Hoffen wir, dass {Role} das Glück beiseite steht!'
    }

    texte = [
        werwolftext, specialText, seeingText, dyingText, oneHitText, restText
    ]
    emojis = [
        werwolfEmojis, specialEmojis, seeingEmojis, dyingEmojis, oneHitEmojis,
        restEmojis
    ]

    def get_help_text(self):
        return self.help_text

    def get_game_start_text(self):
        return self.game_start_text

    def get_game_end_text(self):
        return self.game_end_text

    def get_character_menu_text(self):
        return self.texte

    def get_character_menu_emojis(self, text):
        return self.emojis[self.texte.index(text)]

    def get_clear_text(self):
        return self.game_clear_text

    def get_emojidict(self):
        return self.emojidict_id
	
    def get_game_join_text(self):
        return self.game_join_text
	
    def get_game_player_role_count_text(self):
        return self.game_player_role_count_text

    def get_name_dict(self):
        return self.namedict

    def get_text_dict(self):
        return self.textdict
    
    def get_common_text_dict(self):
        return self.commontextdict
    
    def get_confirm_menu_dict(self):
        return self.confirmmenudict
    
    def get_game_end_safety_question_text(self):
        return self.game_end_safety_question_text

    def get_ynemojis(self):
        return self.ynemojis
    
    def get_erzaehler_commands_text(self):
        return self.erzaehler_commands_text

    def get_numbered_emojis(self):
        return self.werwolfEmojis
    
    def get_death_text_dict_day(self):
        return self.deathtextdict_day
    
    def get_death_text_dict_night(self):
        return self.deathtextdict_night

    def get_death_text_dict_pair(self):
        return self.pairtextdict

        
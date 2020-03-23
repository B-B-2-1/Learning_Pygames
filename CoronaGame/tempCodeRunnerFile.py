    for bed in beds:
        bed.drawBed(win)
        if bed.playerclose(nurse):
            messageDisplay("collision")

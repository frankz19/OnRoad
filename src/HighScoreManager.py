import src.utilities.highscores as HighScore

class HighScoreManager:
    @classmethod
    def get_max_score(cls) -> int:
        """Obtiene el puntaje más alto actual de la tabla oficial del juego."""
        hs = HighScore.read_highscores()
        if hs and len(hs) > 0:
            # El primer elemento de la lista es el puntaje más alto (nombre, puntaje)
            return hs[0][1]
        return 0

    @classmethod
    def get_unlocked_bikes(cls) -> list:
        """Calcula dinámicamente las motos desbloqueadas basándose en el récord máximo."""
        max_score = cls.get_max_score()
        unlocked = [0] # La Socialist (0) siempre está disponible
        
        # Umbrales oficiales de desbloqueo
        if max_score >= 250:
            unlocked.append(1) # SBR
        if max_score >= 500:
            unlocked.append(2) # Enduro
        if max_score >= 800:
            unlocked.append(3) # Hyper Beast
            
        return unlocked
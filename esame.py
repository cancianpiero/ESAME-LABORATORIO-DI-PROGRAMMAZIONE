class ExamException(Exception):
    pass

class CSVTimeSeriesFile:

    def __init__(self, name):
        #controllo che l'oggetto sia una stringa
        if((isinstance(name, str))!=True): 
            raise ExamException("Il nome del file non è valido")
        else:
            self.name = name

    def get_data(self):
        
        #creo una lista vuota
        time_series = []

        #provo ad aprire il file
        try:
            time_series_file = open(self.name, 'r')
        except:
            raise ExamException("Errore nell'apertura del file")
        
        # Ora inizio a leggere il file linea per linea
        for line in time_series_file:
            # Faccio lo split di ogni linea sulla virgola
            elements = line.split(',')
            # Se NON sto processando l'intestazione...
            if elements[0] != 'epoch':
                # Setto timestamp e temperature
                try:
                    timestamp = int(elements[0])
                    temperature = float(elements[1])
                    time_series.append([timestamp,temperature])

                except:
                    print('la riga non è valida')
                
        # Chiudo il file
        time_series_file.close()

        #controllo che i timestamp siano ordinati e che non ci siano doppioni
        for i in range (len(time_series)-1):
            if time_series[i][0] >= time_series[i+1][0]:
                raise ExamException("i timestamps non sono validi")

        # Quando ho processato tutte le righe, ritorno i time_series
        return time_series


def daily_stats(time_series):

    day_start = [] #lista che contiene l'inizio dei vari giorni
    stats =[] #statistiche giornaliere

       #prendo tutti gli epoch del time_series e guardo quali appartengono a ciascun giorno
    for epoch in time_series:
        day_start_epoch = epoch[0] - (epoch[0] % 86400)

        if day_start_epoch not in day_start:
            day_start.append(day_start_epoch)

    #costruisco la funzione che mi calcola le statistiche giornaliere
    for j in range(len(day_start)):
        day = []
        for i in range(len(time_series)):
            #guardo se la misurazione appartiene a quel giorno
            if day_start[j] == (time_series[i][0] - (time_series[i][0] % 86400)):
                day.append(time_series[i][1])
        #aggiungo temperatura minima, massima, media
        stats.append([min(day), max(day), sum(day)/len(day)])

    #ritorno una lista di liste contenente le statistiche giornaliere
    return stats





   

    
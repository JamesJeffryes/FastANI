# This class is responsible for parsing and pretty-printing the text output from FastANI

class FastANIOutput:

    def __init__(self, output):
        self.raw_output = output
        self.get_results(output)
        self.get_summary()
    
    def get_results(self, output):
        '''
        Parse and save an array of results
        '''
        entries = output.split("\n")
        self.results = []
        for line in entries[:-1]:
            parts = line.split(" ")
            self.results.append({
                'query': parts[0],
                'reference': parts[1],
                'percentage_match': parts[2],
                'orthologous_matches': parts[3],
                'total_fragments': parts[4]
            })
        return self

    def get_summary(self):
        self.summary = 'Total results: ' + str(len(self.results))
        for result in self.results:
            self.summary += '\n\n'
            self.summary += ''.join([
                'Query: ', result['query'], '\n',
                'Reference: ', result['reference'], '\n',
                'ANI Estimate: ', result['percentage_match'], '\n',
                'Total fragments: ', result['total_fragments'], '\n',
                'Orthologous matches: ', result['orthologous_matches']
            ])
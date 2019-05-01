import nav.adjust as adjust
import nav.predict as predict
import nav.correct as correct
import nav.locate as locate

def dispatch(values=None):

    #Validate param
    if(values == None):
        return {'error': 'parameter is missing'}
    if(not(isinstance(values,dict))):
        return {'error': 'parameter is not a dictionary'}
    if (not('op' in values)):
        values['error'] = 'no op  is specified'
        return values

    #Perform designated function
    if(values['op'] == 'adjust'):
        result = adjust.adjust(values)
        return result    
    elif(values['op'] == 'predict'):
        result = predict.predict(values)
        return result
    elif(values['op'] == 'correct'):
        result = correct.correct(values)
        return result
    elif(values['op'] == 'locate'):
        result = locate.locate(values)
        return result
    else:
        values['error'] = 'op is not a legal operation'
        return values

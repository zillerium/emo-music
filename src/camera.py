import cv2
import logging
import time
import ast
from get_face import get_attributes
import cognitive_face as CF

logger = logging.getLogger()
hdlr = logging.FileHandler('./log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

KEY = '6c6706553c864529901bddd38b1fb24d'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.list_dict_emotions = []
        self.time_steps = 10
       
    def __del__(self):
        self.video.release()


    def get_confidence(self, time_steps, allEmotions):
        """ Compute the confidence across the previous time_steps """

        # List of all 8 emotions 
        list_all_emotions = [e for e in allEmotions[0]['scores']]

        # List of dictionaries with keys and values
        list_metrics = [i['scores'] for i in allEmotions]

        # Confidence average across dictionaries / faces in the image
        sum_confidence = [sum(d[i] for d in list_metrics) / len(list_metrics) for i in list_all_emotions]

        # Converts the confidence vector to a dictionary
        dict_emotions = {}
        for i in range(len(list_all_emotions)):
            dict_emotions[list_all_emotions[i]] = sum_confidence[i]

        # Append the dictionary to the list with all dictionaries
        self.list_dict_emotions.append(dict_emotions)

        # Gets top time_steps entries in the emotions list. 
        last_five_entries = self.list_dict_emotions[-time_steps:]

        # Get the average across the previous time_steps entries, as a vector of confidence scores. 
        last_five_entries_avg = [float(sum(d[j] for d in self.list_dict_emotions)) / len(self.list_dict_emotions) for j in list_all_emotions]

        # Builds the returned vector into a final dictionary with emotions as labels and confidence as values
        final_dict = {}

        for i in range(len(list_all_emotions)):
            final_dict[list_all_emotions[i]] = last_five_entries_avg[i]

        # Prints the result
        #print(final_dict)

        # Gets the most probable emotion across the previous time_steps 
        #overall_sentiment = max(final_dict.items(), key=operator.itemgetter(1))[0]

        return final_dict #overall_sentiment
    
    
    def get_frame(self):
        #personGroupId = 'myfriends'

        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)

        #cv2.imwrite("test.jpg", image)

        jpeg_bytes = jpeg.tobytes()
        #gets a list of the faces it's found in the webcam shot
        out_str = get_attributes(jpeg_bytes)
        steps = self.time_steps
         
        out_dict = ast.literal_eval(out_str)
        
        if len(out_dict) > 0:
            print "Persisted prediction"
            print self.get_confidence(time_steps=steps, allEmotions=out_dict)



        #if len(out) > 0:
            #logger.info(out[0]['faceAttributes']['emotion']['surprise'])
            #logger.info(out)
            #faceIds = [x['faceId'] for x in out]
            #logger.info(out)
            #logger.info(faceIds)

            #results = CF.face.identify(faceIds, personGroupId);

            #logger.info(results)
            # for identifyResult in results :
            #     logger.info("Result of face: " + identifyResult['faceId']);
            #     if (identifyResult['Candidates'].Length == 0)
            #     {
            #         Console.WriteLine("No one identified");
            #     }
            #     else
            #     {
            #         // Get top 1 among all candidates returned
            #         var candidateId = identifyResult.Candidates[0].PersonId;
            #         var person = await faceServiceClient.GetPersonAsync(personGroupId, candidateId);
            #         Console.WriteLine("Identified as {0}", person.Name);
            #     }
            


   
        time.sleep(4)
        #send image to API and compare against participants

        return jpeg_bytes

import 'package:get/get.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:permission_handler/permission_handler.dart';

class AudioController extends GetxController {
  var isListening = false.obs;
  var speechText = "Speak......";
  SpeechToText speechToText = SpeechToText();

  Future<void> checkPermissions() async {
    var status = await Permission.microphone.request();
    if (!status.isGranted) {
      print("Microphone permission not granted");
      // Notify the user or open settings
    }
  }

  void listen() async {
    await checkPermissions();
    isListening.value = true;
    bool available = await speechToText.initialize(
      onError: (val) {},
      onStatus: (val) {},
    );
    if (available) {
      await speechToText.listen(onResult: (val) {
        speechText = val.recognizedWords;
      });
    }
  }

  void notListen() async {
    isListening.value = false;
    await speechToText.stop();
  }
}

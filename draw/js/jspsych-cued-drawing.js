/*
 * Example plugin template
 */

jsPsych.plugins["jspsych-cued-drawing"] = (function() {

  var plugin = {};

  plugin.info = {
    name: "jspsych-cued-drawing",
    parameters: {
      cue_label: {
        type: jsPsych.plugins.parameterType.STRING, // BOOL, STRING, INT, FLOAT, FUNCTION, KEYCODE, SELECT, HTML_STRING, IMAGE, AUDIO, VIDEO, OBJECT, COMPLEX
        pretty_name: 'cue_label',
        default: undefined,
        description: 'The label used to cue drawing.'
      }, 
      cue_image: {
        type: jsPsych.plugins.parameterType.IMAGE,
        pretty_name: 'cue_image',
        default: undefined,
        description: 'The image used to cue drawing.'
      }, 
      cue_image_url: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'cue_image_urls',
        default: undefined,
        array: true,
        description: 'The URL for the image cues.'
      },
      cue_video: {
        type: jsPsych.plugins.parameterType.VIDEO,
        pretty_name: 'cue_video',
        default: undefined,
        description: 'The video used to cue drawing.'
      }, 
      cue_duration: {
        type: jsPsych.plugins.parameterType.INT,
        pretty_name: 'cue_duration',
        default: null,
        description: 'How long to show the cue (in milliseconds).'
      }, 
      prompt: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'prompt',
        default: null,
        description: 'What to display to the participant as the instructions.'
      }                       
    }
  }

  plugin.trial = function(display_element, trial) {

    if(typeof trial.cue_label === 'undefined'){
      console.error('Required parameter "cue_label" missing in jspsych-cued-drawing');
    }

    // wrapper function to show everything, call this when you've waited what you
    // reckon is long enough for the data to come back from the db
    function show_display() { 

      // display cue

      // display prompt

      // display canvas

      // display 

    }



    // data saving
    var trial_data = {
      parameter_name: 'parameter value'
    };

    // end trial
    jsPsych.finishTrial(trial_data);
  };

  return plugin;
})();

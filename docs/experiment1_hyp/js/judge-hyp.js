/**
 * a jspsych plugin for hypothetical judgment slider question
 *
 */


jsPsych.plugins['judge-hyp'] = (function() {

  var plugin = {};

  plugin.info = {
    name: 'judge-hypothetical',
    description: '',
    parameters: {
      trial: {
        type: jsPsych.plugins.parameterType.HTML_STRING,
        pretty_name: 'Trial',
        default: null,
        description: 'Trial number'
      },
      title: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Title',
        default: ' ',
        description: ''
      },
      path: {
        type: jsPsych.plugins.parameterType.STRING,
        pretty_name: 'Path',
        default: ' ',
        description: ''
      }
    }
  }

  var slider_width = 500;
  var slider_labels = ['not at all', 'very much'];
  var button_label = 'Continue';

  plugin.trial = function(display_element, trial) {

    var html = '<div id="jspsych-html-slider-response-wrapper">';
    html += '<div id="jspsych-html-slider-response-stimulus">';
    html += '<h2>' + trial.title + '</h2>';
    html += '<img src="trials/' + trial.trial + '/00.png"></img></div>';
    html += '<p> To what extent do you agree with the following statement? </p>';
    html += '<p> <q>The player would win if they took the ' + trial.path + ' path this time. </q> </p>';
    html += '<div class="jspsych-html-slider-response-container" style="position:relative; margin: 0 auto 2em auto; width:' + slider_width + 'px;">';

    html += '<div style="width: 100%;" id="jspsych-html-slider-response-response"></div>';
    html += '<div>'
    for(var j=0; j < slider_labels.length; j++){
      var width = 100/(slider_labels.length-1);
      var left_offset = (j * (100 /(slider_labels.length - 1))) - (width/2);
      html += '<div style="display: inline-block; position: absolute; left:'+left_offset+'%; text-align: center; width: '+width+'%;">';
      html += '<span style="text-align: center; font-size: 80%;">'+slider_labels[j]+'</span>';
      html += '</div>'
    }
    html += '</div>'; // for response container
    html += '</div>'; // for response wrapper
    html += '</div>';

    // add submit button
    html += '<button id="jspsych-html-slider-response-next" class="jspsych-btn" disabled>'+button_label+'</button>';

    display_element.innerHTML = html;

    var response = {};

    set_slider();

    display_element.querySelector('#jspsych-html-slider-response-next').addEventListener('click', function() {
      response.slider = $('#jspsych-html-slider-response-response').slider('option', 'value');
      end_trial();
    });

    function end_trial(){

      jsPsych.pluginAPI.clearAllTimeouts();

      // save data
      var trialdata = {
        "trial": trial.trial,
        "response": response.slider
      };

      display_element.innerHTML = '';

      // next trial
      jsPsych.finishTrial(trialdata);
    }

  };

  return plugin;
})();

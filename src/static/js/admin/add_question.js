var questionApp = angular.module('questionApp', []);

questionApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});

questionApp.filter('objectiveFilter', function () {
    return function (exams, value) {
        if (value === "") {
            return exams;
        }
        var examArray = [];
        var mappings = { "true": true, "false": false };
        angular.forEach(exams, function (exam) {
            if (exam.objective === mappings[value]) {
                examArray.push(exam);
            }
        });
        return examArray;
    };
});

questionApp.controller('QuestionController', function ($scope, $http) {
    $scope.examType = "";
    var obj_api = '/_ah/api/objective/v1/objectives/';
    var essay_api = '/_ah/api/essay/v1/essays/';

	$http.get('/_ah/api/examiner/v1/examiners').success(function(data){
		$scope.examiners = data.items;
	});
	$http.get('/_ah/api/subject/v1/subjects').success(function(data){
		$scope.subjects = data.items;
	});

	// watch examiner and subject for changes and update exams
	$scope.$watchCollection('[selected_examiner, selected_subject]', function(newValue){
		if ( $scope.selected_examiner && $scope.selected_subject ){
			$http.get('/_ah/api/exam/v1/exams', {params: 
				{examiner: $scope.selected_examiner.entityKey, 
					subject: $scope.selected_subject.entityKey}}).success(function(data){
						$scope.exams = data.items? data.items: null;
					}).error(function(data){
						$scope.exams = null;
					});
		}else{
			$scope.exams = null;
		}
	});

	$scope.$watch('exams', function(){
		$scope.selected_exam = null;
	});

	// watch selected_exam for change and update questions
	$scope.$watch('selected_exam', function(){
	    if ($scope.selected_exam) {
	        if (($scope.selected_exam).objective) {
	            var url = obj_api;
	        } else if (!($scope.selected_exam).objective) {
	            var url = essay_api;
	        } else {
	            return;
	        }
			$http.get(url, {params: 
				{exam: $scope.selected_exam.entityKey, order:'number'}}).success(function(data){
						$scope.questions = data.items? data.items: null;
						$scope.selected_question = null;
					}).error(function(data){
						$scope.questions = null;
						$scope.selected_question = null;
					});
		}else{
			$scope.questions = null;
			$scope.selected_question = null;
		}
	});

	// watch the selected question and update accordingly
	$scope.$watch('selected_question', function (new_question, old_question) {
	    if (new_question && $scope.newly_selected_index != -1) {
	        ($scope.questions)[$scope.newly_selected_index] = old_question; // keep any change in memory
	    }	    
	    $scope.newly_selected_index = -1;
		if(new_question){
			$scope.new_number = new_question.number;
		}else{
			$scope.new_number = null;
		}
		if ($scope.questions) {
		    $scope.newly_selected_index = $scope.questions.indexOf(new_question); // store index of new question
		}
		if (new_question && ($scope.selected_exam).objective && $scope.newly_selected_index) {
			$scope.trimChoices(); // ensure number of options is number of selected_exam options
		}
	});
	

	$scope.trimChoices = function(){ //assumes selected_question and index are valid
		var no_choices = ( ( $scope.selected_question ).choices ).length;
		if ( no_choices > parseInt(($scope.selected_exam).no_choices) ){
			( $scope.selected_question ).choices = (($scope.selected_question).
											choices).slice(0, ($scope.selected_exam).no_choices) ;
		}else if( no_choices < parseInt(($scope.selected_exam).no_choices) ){
			var difference = ($scope.selected_exam).no_choices - no_choices;
			for (i=0; i < difference; i++){
				var init_choice = {text:""} ;
				( ($scope.selected_question).choices ).push(init_choice);
			}
		}
	}
	$scope.validateRightChoice = function(){
		if (($scope.selected_question).right_choice === "" || ! ($scope.selected_question).right_choice){
			($scope.selected_question).right_choice = null;
			return true;
		}
		var right_choice = parseInt(($scope.selected_question).right_choice);
		if (right_choice){ // was a valid integer and wasn't null
			if( right_choice > 0 && right_choice <= ($scope.selected_exam).no_choices){
				return true; 
			}else{
				($scope.selected_question).right_choice = null;
				return false;
			}
		}else{
			return false;
		}
	}
	$scope.updateQuestion = function(){
		if ($scope.selected_question){ //valid question selection
			if (! $scope.validateRightChoice()){
				alert("Invalid Right Choice");
				return;
			}
			if (($scope.selected_exam).objective) {
			    var url = obj_api;
			} else if (!($scope.selected_exam).objective) {
			    var url = essay_api;
			} else {
			    return;
			}
			$http.post(url, $scope.selected_question).success(function(data){
				$scope.selected_question = data;
				($scope.selected_question) = data;
				$scope.addOrDisplay();

			}).error(function(data){
				alert(data.error.message);
			});
		}
	}

	$scope.addOrDisplay = function(){
		if ($scope.selected_exam){  //only update if an exam has been selected
			var new_number = parseInt($scope.new_number);
			if( ! isNaN(new_number) && new_number < 100 && new_number >=0){
				$scope.new_number = new_number;
				var question_exists = false;
				if( $scope.questions){ //ensure there are questions 
					var num_questions = ($scope.questions).length;
					for ( i=0; i < num_questions; i++){
						if (new_number == ( ($scope.questions)[i] ).number ){
							question_exists = true;
							$scope.selected_question = ($scope.questions)[i];
							break;
						}
					}
				}
				if(! question_exists ){ // create new question
					var choices = [];
					for (i=0; i < parseInt( ($scope.selected_exam).no_choices); i++){
						var init_choice = {text:""} ;
						choices.push(init_choice);
					}
					var new_question = {number: new_number, choices:choices,
						tags:[], exam: $scope.selected_exam.entityKey};
					if(! $scope.questions){ //questions was null
						$scope.questions = [];
						$scope.questions.push(new_question);
						$scope.selected_question = ($scope.questions)[0];
					}else{
						$scope.questions.push(new_question);
						var num_questions = ($scope.questions).length ;
						$scope.selected_question = ($scope.questions)[num_questions-1]; // zero index based
					}
					
					
				}
			}else{
				if ($scope.selected_question){
					$scope.new_number = $scope.selected_question.number;
					alert("Invalid Question Number");
				}
			}
		}
	};
	$scope.appendTags = function(){
		if (! (($scope.selected_question).tags)){
			(($scope.selected_question).tags) = [];
		}
		if ($scope.new_tag){
			if ( (($scope.selected_question).tags).indexOf($scope.new_tag) === -1){
				(($scope.selected_question).tags).push($scope.new_tag);
			}
		}
	}

});



// Begin latex stuff

var Preview = {
  delay: 150,        // delay after keystroke before updating

  preview: null,     // filled in by Init below
  buffer: null,      // filled in by Init below

  timeout: null,     // store setTimout id
  mjRunning: false,  // true when MathJax is processing
  oldText: null,     // used to check if an update is needed

  //
  //  Get the preview and buffer DIV's
  //
  Init: function () {
    this.preview = document.getElementById("MathPreview");
    this.buffer = document.getElementById("MathBuffer");
  },

  //
  //  Switch the buffer and preview, and display the right one.
  //  (We use visibility:hidden rather than display:none since
  //  the results of running MathJax are more accurate that way.)
  //
  SwapBuffers: function () {
    var buffer = this.preview, preview = this.buffer;
    this.buffer = buffer; this.preview = preview;
    buffer.style.visibility = "hidden"; buffer.style.position = "absolute";
    preview.style.position = ""; preview.style.visibility = "";
  },

  //
  //  This gets called when a key is pressed in the textarea.
  //  We check if there is already a pending update and clear it if so.
  //  Then set up an update to occur after a small delay (so if more keys
  //    are pressed, the update won't occur until after there has been 
  //    a pause in the typing).
  //  The callback function is set up below, after the Preview object is set up.
  //
  Update: function () {
    if (this.timeout) {clearTimeout(this.timeout)}
    this.timeout = setTimeout(this.callback,this.delay);
  },

  //
  //  Creates the preview and runs MathJax on it.
  //  If MathJax is already trying to render the code, return
  //  If the text hasn't changed, return
  //  Otherwise, indicate that MathJax is running, and start the
  //    typesetting.  After it is done, call PreviewDone.
  //  
  CreatePreview: function () {
    Preview.timeout = null;
    if (this.mjRunning) return;
    var text = document.getElementById("MathInput").value;
    if (text === this.oldtext) return;
    this.buffer.innerHTML = this.oldtext = text;
    this.mjRunning = true;
    MathJax.Hub.Queue(
      ["Typeset",MathJax.Hub,this.buffer],
      ["PreviewDone",this]
    );
  },

  //
  //  Indicate that MathJax is no longer running,
  //  and swap the buffers to show the results.
  //
  PreviewDone: function () {
    this.mjRunning = false;
    this.SwapBuffers();
  }

};

//
//  Cache a callback to the CreatePreview action
//
Preview.callback = MathJax.Callback(["CreatePreview",Preview]);
Preview.callback.autoReset = true;  // make sure it can run more than once

app.controller('main', function($scope) {

  $scope.currentState = {};
  $scope.requests = [];
  $scope.isShuffled = false;
  $scope.isPlaying = false;
  $scope.requestUrl = "index.html";

  $scope.callbacks = {
    "next_album" : function(data) {
      if( data && data["output"] ) {
        $scope.currentPlaylist = data["output"];
      }
    },
    
    "prev_album" : function(data) {
      if( data && data["output"] ) {
        $scope.currentPlaylist = data["output"];
      }
    },

    "refresh_data" : function() {
      $scope.syncPlayer();
    }

  }
  
  // Wrapper for button clicks to disable actions 
  // until all of the requests are resolved
  $scope.buttonPlayerAction = function( action, callback ) {
    if( !$scope.requests.length ) {
      $scope.playerAction( action, callback )
    }
  }
   
  // Perform a network action with the server
  $scope.playerAction = function( action, callback) {
    if( typeof callback === "undefined" ) {
      callback = function(d){ console.log(d); };
    }
        
    var request = $.ajax({
      type: "POST",
      url: $scope.requestUrl,
      data: { action: action },
      timeout: 5000
    })
    .done(callback)
    .always(function(data){
      // Provide a action callback if it is defined
      if( typeof $scope.callbacks[action] === "function" ) {
        $scope.callbacks[action]( data );
      }
      $scope.requests.pop();
      $scope.$apply();
    });
    
    $scope.requests.push( request );
  };
  
  $scope.syncPlayer = function(){
    $scope.playerAction( "info", function(data){
      if( data && data["output"] ) {
        //setTimeout( $scope.syncPlayer, 2000 );
        $scope.currentState = data["output"];
        $scope.$apply();
      }
    });   
  };
    
  $scope.syncPlayer();
  setTimeout( $scope.syncPlayer, 2000 );

});

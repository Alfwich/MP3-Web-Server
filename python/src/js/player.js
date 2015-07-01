app.controller('main', function($scope) {

  $scope.currentState = {};
  $scope.requests = [];
  $scope.syncHandle = null;
  $scope.requestUrl = "index.html";

  $scope.callbacks = {
    "next_album" : function(data) {
      $scope.syncPlayer();    
    },
    
    "prev_album" : function(data) {
      $scope.syncPlayer();    
    },

    "refresh_data" : function() {
      $scope.syncPlayer();
    }

  }
  
  $scope.processTime = function(t) {
    var result = null;
    
    if( t && typeof t === "string" ) {
      var comps = t.split(":");
      if( comps.length == 2 ) {
        result = parseInt(comps[0])*60 + parseInt(comps[1]);
      }
    }
  
    return result;
  }
  
  $scope.computeDuration = function() {
    var currentTime = $scope.processTime( $scope.currentState.currenttime ),
        totalTime = $scope.processTime( $scope.currentState.totaltime ),
        result = 0;
    
    if( currentTime !== null && totalTime !== null ) {
      result = currentTime / totalTime * 100;
    }
    
    return result + "%";
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
        clearTimeout( $scope.syncHandle );
        $scope.syncHandle = setTimeout( $scope.syncPlayer, 2000 );
        $scope.currentState = data["output"];
        $scope.$apply();
      }
    });   
  };
    
  $scope.syncPlayer();
});

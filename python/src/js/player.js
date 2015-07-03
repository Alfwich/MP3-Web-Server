(function(){

  app.controller('main', function($scope) {

    $scope.currentState = {};
    $scope.requests = [];
    $scope.syncHandle = null;
    $scope.requestUrl = "/";

    // Get the saved requestUrl from localstorage if it exists
    if( localStorage ) {
      var item;
      if( item = localStorage.getItem("MP3-OVERRIDE-URL")) {
        console.log( "Replacing requestUrl with the provided url: " + item );
        $scope.requestUrl = item;
      }
    }

    $scope.getProgressText = function() {
      var result = [];

      if( $scope.currentState["artist"] ) {
        result.push( $scope.currentState["artist"] );
      }

      if( $scope.currentState["songtitle"] ) {
        result.push( $scope.currentState["songtitle"] );
      }

      return result.join(", ") || "No Title";
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

        // Sync the player if this was not a info action
        if( action !== "info" ) {

          // Wrap the sync call in a timeout to allow the effects
          // of the previous action to take effect
          setTimeout( function() {
            $scope.syncPlayer();
          }, 250 );
        }

        $scope.requests.pop();
        $scope.$apply();
      });

      $scope.requests.push( request );
    };

    $scope.syncPlayer = function(){
      $scope.playerAction( "info", function(data){
        if( data && data["output"] ) {
          $scope.currentState = data["output"];
          var current = parseInt($scope.currentState.currentsec),
              total = parseInt($scope.currentState.totalsec);
          clearTimeout( $scope.syncHandle );

          // Setup the info callback to happen 1 seconds after the song ends
          $scope.syncHandle = setTimeout( $scope.syncPlayer, (total-current+1)*1000 );
        }
      });
    };

    $scope.syncPlayer()
  });
})()

var page = require('webpage').create(),
	system = require('system');
page.settings.userAgent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36';
page.open(system.args[1],function(status){
	var title = page.evaluate(function(){
	return document.title;
	});
	console.log('Page title is ' + title);
	phantom.exit();
});

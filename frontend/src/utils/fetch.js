
export function fetchData(url, data, options = {}) {
	options.credentials = 'include'
	options.headers = { 'Access-Control-Allow-Origin': '*' }
	if (data) {
		options.body = JSON.stringify(data)
	}
	if (options.method === 'POST') {
		options.headers['Content-Type'] = 'application/x-www-form-urlencoded'
	}
	return new Promise((resolve, reject) => {
		fetch(url, options).then(res => {
			res.json().then(json => {
				resolve(json);
			});
		}).catch(error => {
			reject(error)
		}).finally(() => { });
	});
}

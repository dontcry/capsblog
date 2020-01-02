import {
	fetchData
} from './fetch';

const baseUrl = 'http://127.0.0.1:5000/api'
// blog api
export const getBlogs = () => {
	const url = `${baseUrl}/blogs`
	return fetchData(url);
};
 
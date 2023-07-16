import request from '@/api/request'

export function chat(data:any){
	return request({
		url: '/',
		method: "post",
		data
	})
}
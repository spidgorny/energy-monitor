import {Injectable} from '@angular/core';

@Injectable()
export class MailService {

	messages = [
		{id: 1, text: 'New mail'},
		{id: 2, text: 'bla'},
		{id: 3, text: 'bla 2'},
	];

	constructor() {
	}

	update(id, text) {
		this.messages = this.messages.map(m => {
			return m.id === id
			? {id, text}
			: m;
		});
	}

}

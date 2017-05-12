import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
	selector: 'app-consumption',
	templateUrl: './consumption.component.html',
	styleUrls: ['./consumption.component.css']
})
export class ConsumptionComponent implements OnInit {

	@Input() message;
	@Output() update = new EventEmitter();

	constructor() {
	}

	ngOnInit() {
	}

	onClick(event, value) {
		console.log(value);
	}

}

import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
	selector: 'app-consumption',
	templateUrl: './consumption.component.html',
	styleUrls: ['./consumption.component.css']
})
export class ConsumptionComponent implements OnInit {

	@Input() message;
	@Output() update = new EventEmitter();

	image_file: string;

	constructor() {
		console.log('constructor');
		this.image_file = 'assets/project_incubator_graphWeekly.png';
	}

	ngOnInit() {
		console.log('ngOnInit');
		this.setTimeout();
	}

	setTimeout() {
		setTimeout(this.refresh.bind(this), 1000);
	}

	onClick(event, value) {
		console.log(value);
	}

	refresh() {
		if (Math.random() > 0.5) {
			this.image_file = 'assets/project_incubator_graphWeekly.png';
		} else {
			this.image_file = 'assets/energy_graph.png';
		}
		this.setTimeout();
	}

}

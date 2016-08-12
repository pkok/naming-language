import shuffle from 'lodash/shuffle';
import sortBy from 'lodash/sortby';
import sortedUniq from 'lodash/sorteduniq';
import {
	defaultOrtho,
	corthsets,
	vorthsets,
	consets,
	ssets,
	lsets,
	fsets,
	vowsets,
	syllstructs,
	ressets,
	joinsets
} from './sources';

function choose( list, exponent = 1 ) {
	return list[ Math.floor( Math.pow( Math.random(), exponent ) * list.length ) ];
}

function randrange( lo, hi = 0 ) {
	return Math.floor( Math.random() * ( hi - lo ) ) + lo;
}

function capitalize( word = '' ) {
	if ( word.length < 2 ) {
		return word;
	}
	return word[ 0 ].toUpperCase() + word.slice( 1 );
}

class Language {
	constructor() {
		this.phonemes = {
			C: 'ptkmnls',
			V: 'aeiou',
			S: 's',
			F: 'mn',
			L: 'rl',
		};
		this.structure = 'CVC';
		this.exponent = 2;
		this.restricts = [];
		this.cortho = {};
		this.vortho = {};
		this.noortho = true;
		this.nomorph = true;
		this.nowordpool = true;
		this.minsyll = 1;
		this.maxsyll = 1;
		this.morphemes = {};
		this.words = {};
		this.names = [];
		this.joiner = ' ';
		this.maxchar = 12;
		this.minchar = 5;
	}

	makeOrthoLanguage() {
		this.noortho = false;
	}

	makeRandomLanguage() {
		this.noortho = false;
		this.nomorph = false;
		this.nowordpool = false;
		this.phonemes.C = shuffle( choose( consets, 2 ).C );
		this.phonemes.V = shuffle( choose( vowsets, 2 ).V );
		this.phonemes.L = shuffle( choose( lsets, 2 ).L );
		this.phonemes.S = shuffle( choose( ssets, 2 ).S );
		this.phonemes.F = shuffle( choose( fsets, 2 ).F );
		this.structure = choose( syllstructs );
		this.restricts = ressets[ 2 ].res;
		this.cortho = choose( corthsets, 2 ).orth;
		this.vortho = choose( vorthsets, 2 ).orth;
		this.minsyll = randrange( 1, 3 );
		if ( this.structure.length < 3 ) {
			this.minsyll++;
		}
		this.maxsyll = randrange( this.minsyll + 1, 7 );
		this.joiner = choose( joinsets );
	}

	spell( syll ) {
		if ( this.noortho ) {
			return syll;
		}
		let s = '';
		for ( let i = 0; i < syll.length; i++ ) {
			const c = syll[ i ];
			s += this.cortho[ c ] || this.vortho[ c ] || defaultOrtho[ c ] || c;
		}
		return s;
	}

	makeSyllable() {
		while ( true ) {
			let syll = '';
			for ( let i = 0; i < this.structure.length; i++ ) {
				const ptype = this.structure[ i ];
				if ( this.structure[ i + 1 ] == '?' ) {
					i++;
					if ( Math.random() < 0.5 ) {
						continue;
					}
				}
				syll += choose( this.phonemes[ ptype ], this.exponent );
			}
			let bad = false;
			for ( let i = 0; i < this.restricts.length; i++ ) {
				if ( this.restricts[ i ].test( syll ) ) {
					bad = true;
					break;
				}
			}
			if ( bad ) {
				continue;
			}
			return this.spell( syll );
		}
	}

	getMorpheme( key = '' ) {
		if ( this.nomorph ) {
			return this.makeSyllable();
		}
		const list = this.morphemes[ key ] || [];
		let extras = 10;
		if ( key ) {
			extras = 1;
		}
		while ( true ) {
			const n = randrange( list.length + extras );
			if ( list[ n ] ) {
				return list[ n ];
			}
			const morph = this.makeSyllable();
			let bad = false;
			for ( const k in this.morphemes ) {
				if ( this.morphemes[ k ].includes( morph ) ) {
					bad = true;
					break;
				}
			}
			if ( bad ) {
				continue;
			}
			list.push( morph );
			this.morphemes[ key ] = list;
			return morph;
		}
	}

	makeWord( key ) {
		const nsylls = parseInt( randrange( randrange( this.minsyll, this.maxsyll + 1 ) ), 10 );
		const keys = [];
		keys[ nsylls ] = key;
		let w = '';
		for ( let i = 0; i < nsylls; i++ ) {
			w += this.getMorpheme( keys[ i ] );
		}
		return w;
	}

	getWord( key = '' ) {
		const ws = this.words[ key ] || [];
		let extras = 3;
		if ( key ) {
			extras = 2;
		}
		while ( true ) {
			const n = randrange( ws.length + extras );
			let w = ws[ n ];
			if ( w ) {
				return w;
			}
			w = this.makeWord( key );
			let bad = false;
			for ( const k in this.words ) {
				if ( this.words[ k ].includes( w ) ) {
					bad = true;
					break;
				}
			}
			if ( bad ) {
				continue;
			}
			ws.push( w );
			this.words[ key ] = ws;
			return w;
		}
	}

	makeName( key ) {
		this.genitive = this.genitive || this.getMorpheme( 'of' );
		this.definite = this.definite || this.getMorpheme( 'the' );
		while ( true ) {
			let name = null;
			if ( Math.random() < 0.5 ) {
				name = capitalize( this.getWord( key ) );
			} else {
				const w1 = capitalize( this.getWord( Math.random() < 0.6 ? key : '' ) );
				const w2 = capitalize( this.getWord( Math.random() < 0.6 ? key : '' ) );
				if ( w1 == w2 ) {
					continue;
				}
				if ( Math.random() > 0.5 ) {
					name = [ w1, w2 ].join( this.joiner );
				} else {
					name = [ w1, this.genitive, w2 ].join( this.joiner );
				}
			}
			if ( Math.random() < 0.1 ) {
				name = [ this.definite, name ].join( this.joiner );
			}

			if ( ( name.length < this.minchar ) || ( name.length > this.maxchar ) ) {
				continue;
			}
			let used = false;
			for ( let i = 0; i < this.names.length; i++ ) {
				const name2 = this.names[ i ];
				if ( ( name.indexOf( name2 ) != -1 ) || ( name2.indexOf( name ) != -1 ) ) {
					used = true;
					break;
				}
			}
			if ( used ) {
				continue;
			}
			this.names.push( name );
			return name;
		}
	}

	getAlphabet() {
		const partsList = [];
		for ( let i = 0; i < this.structure.length; i++ ) {
			const part = this.structure[ i ];
			if ( 'undefined' !== typeof this.phonemes[ part ] ) {
				partsList.push( ...this.phonemes[ part ] );
			}
		}
		const list = sortBy( partsList );
		return this.spell( sortedUniq( list ).join( ' ' ) );
	}
}

export default Language;

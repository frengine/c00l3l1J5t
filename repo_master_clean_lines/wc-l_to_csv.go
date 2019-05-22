package main

/*
Format the output of "wc -l" (saved to a file) to csv.
*/

import "io/ioutil"
import "fmt"
import "bytes"
import "bufio"
import "strings"

const errmsg = "Oi. Does 1-2_wc-l.txt exist and does it contains the output of 'wc -l .' in the 1-2 directory?"

func main() {
	data, err := ioutil.ReadFile("1-2_wc-l.txt")
	if err != nil {
		fmt.Println(errmsg)
		fmt.Println(err)
		return
	}

	scanner := bufio.NewScanner(bytes.NewReader(data))
	for scanner.Scan() {
		line := scanner.Text()
		line = strings.TrimSpace(line)
		split := strings.Split(line, " ")
		fmt.Printf("%s\t%s\n", split[1], split[0])
	}
}

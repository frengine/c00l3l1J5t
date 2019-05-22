package main

import "path/filepath"
import "log"
//import "fmt"
//import "bufio"
import "os"
import "os/exec"
import "sync"

var projects = []string{"1-2", "2-1", "2-2", "2-3"}

func main() {
	for _, project := range projects {
		err := calculateProject(project)
		if err != nil {
			log.Fatal(err)
		}
	}
}

func calculateProject(project string) error {
	matches, err := filepath.Glob("repo_master_clean_lines/" + project + "/*.txt")
	if err != nil {
		return err
	}

	wg := sync.WaitGroup{}

	const n_per_thread = 5

	amount := len(matches)/n_per_thread+1

	wg.Add(amount-1)

	for i := 0; i < amount; i++  {
		min := i*n_per_thread
		max := (i+1)*n_per_thread
		if (i+1)*5+1 >= len(matches) {
			max = len(matches)-1
		}

		files := matches[min:max]
		iCopy := i

		go func() {
			defer wg.Done()

			log.Println("\n\n\n")
			log.Println(files)

			args := append([]string{"gsheet_master_lines.py", project}, files...)
			cmd := exec.Command("python3", args...)
			cmd.Stdout = os.Stdout
			cmd.Stderr = os.Stderr

			/*stdout, err := cmd.StdoutPipe()
			if err != nil {
				log.Fatal(iCopy, err)
			}*/
			err = cmd.Start()
			if err != nil {
				log.Fatal(iCopy, err)
			}

			log.Println(iCopy, "start")

			/*scanner := bufio.NewScanner(stdout)
			scanner.Split(bufio.ScanWords)
			for scanner.Scan() {
				m := scanner.Text()
				fmt.Println(iCopy, m)
			}
			if scanner.Err() != nil {
				log.Fatal(iCopy, scanner.Err())
			}*/

			cmd.Wait()

			log.Println(iCopy, "yeah")

		}()
	}

	wg.Wait()

	return nil
}
